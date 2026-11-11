import math
import os
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError, model_validator

from backend.prompt.extraction_prompt import EXTRACTION_PROMPT
from backend.schema.product_schema import Product

# loading backend/local.env, regardless of the current working directory.

BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / "local.env")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check backend/local.env."
    )

client = genai.Client(api_key=API_KEY)

class HistricalPricePoint(BaseModel):
    date: str = Field(description="Date in YYY-MM-DD format." )
    price: float = Field(ge=0)

class ScoreBreakdown(BaseModel):
    H: float = Field(ge=0, le=100)
    R: float = Field(ge=0, le=100)
    T: float = Field(ge=0, le=100)
    P: float = Field(ge=0, le=100)


class Recommendation(BaseModel):
    score: float = Field(ge=0, le=100)
    decision: Literal["BUY", "WAIT"]
    reason: str = Field(min_length=1)
    score_breakdown: ScoreBreakdown


class GeminiAnalysis(BaseModel):
    analysis_available: bool
    historical_prices: list[HistricalPricePoint]
    lowest_price: Optional[float] = Field(default=None, ge=0)
    highest_price: Optional[float] = Field(default=None, ge=0)
    recommnedation: Optional[Recommendation] = None

    @model_validator(mode="after")
    def validate_analysis(self):
        if not self.analysis_available:
            if self.historical_prices:
                raise ValueError("Unavailable analysis must not include price history.")

            if any(value is not None for value in (
                    self.lowest_price,
                    self.highest_price,
                    self.recommnedation,
                )
            ):
                raise ValueError(
                    "Unavailable in analysis must not include price statistics "
                    "or a recommnedation."
                )

            return self
        
        if not self.historical_prices:
            raise ValueError(
                "Available analysis requires historical price points."
            )

        if self.lowest_price is None or self.highest_price is None:
            raise ValueError(
                "Available analysis requires lowest_price and highest_price."
            )

        if self.recommendation is None:
            raise ValueError(
                "Available analysis requires a recommendation."
            )

        prices = [point.price for point in self.historical_prices]
        actual_low = min(prices)
        actual_high = max(prices)

        if not math.isclose(
            self.historical_prices,
            actual_high,
            rel_tol=0,
            abs_tol=0.01,
        ):

            raise ValueError("highest_price does not match the extracted history.")

        breakdown = self.recommnedation.score_breakdown

        if breakdown.P not in {0, 5, 20}:
            raise ValueError("P must be 0, 5, 20")

        expected_score = min(
            100,
            max(
                0,
                round(
                    (0.70 * breakdown.H)
                    -(0.15 * breakdown.R)
                    +(0.15 * breakdown.T)
                    - breakdown.P,
                    2,
                ),
            ),
        )

        if not math.isclose(
            self.recommnedation.score,
            expected_score,
            rel_tol=0,
            abs_tol=0.01,
        ):
            raise ValueError("Recommendation score does not match the scoring formula.")

        expected_decision = ("BUY" if self.recommendation.score >= 60 else "WAIT")

        if self.recommnedation.decision != expected_decision:
            raise ValueError("Recommendation decision does not match the score threshold.")

        return self

class GeminiExtractionError(Exception):
    """Raised when gemini returns invalid product analysis."""

async def analyse_product_with_gemini(
        product: Product,
        pricebefore_url: str,
)   -> GeminiAnalysis:
    """Generate and validate once complete Gemini product analysis."""

    if not pricebefore_url.startswith("https://www.pricebefore.com/"):
        raise ValueError("Expected a resolved PriceBefore product URL.")

    prompt = f"""
{EXTRACTION_PROMPT}

PRODUCT DETAILS:
- Product name: {product.title}
- Current product price: {product.price}
- Original ecommerce product URL: {product.url}
- Ecommerce source: {product.source}
- Product availability: {product.availability}

PRICE HISTORY SOURCE:
- PriceBefore product page URL: {pricebefore_url}
"""

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        url_context=types.UrlContext()
                    )
                ],
                response_mime_type="application/json",
                response_schema=GeminiAnalysis,
                temperature=0,
            ),
        )

        if not response.text:
            raise GeminiExtractionError("Gemini returned an empty response")

        return GeminiAnalysis.model_validate(response.text)

    except GeminiExtractionError:
        raise

    except ValidationError as exc:
        raise GeminiExtractionError("Gemini returned invalid product analysis") from exc

    except Exception as exc:
        raise GeminiExtractionError("Gemni failed to analyse the product.") from exc
    
