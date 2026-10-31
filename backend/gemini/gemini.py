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


class GeminiAnalysis(BaseModel)
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

        if not