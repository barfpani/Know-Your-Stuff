import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError

from backend.prompt.extraction_prompt import EXTRACTION_PROMPT

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

class HistoricalPricePoint(BaseModel):
    """One historical product price."""
    data: str = Field(
        description="Date in YYYY-MM-DD format."
    )
    price: float = Field(
        ge=0,
        description="Product price on that date."
    )

class HistoricalPriceExtraction(BaseModel):
    """Historical pricess extracted from a PriceBefore page."""
    historical_prices: list[HistoricalPricePoint] = Field(
        description=(
            "Explicitly available historical price points. "
            "Use as empty list if no reliable history is available."
        )
    )

class GeminiExtractionError(Exception):
    """Raised when Gemini cannt extract valid price histroy."""

async def extract_price_history(
        pricebefore_url: str,
) -> list[dict]:
    """
    Extract historical rice points from a resolved PriceBefore URL.
    
    Returns:
        A list of dictionaries with date and price fields.
        Returns an empty list when no history is available.
        
    Raises:
    GeminiExtractionError: If the API call or validation fails
    """

    if not pricebefore_url.startswith("https://www.pricebefore.com/"):
        raise ValueError("Exected a resolved PriceBefore product URL.")

    prompt = (
        f"{EXTRACTION_PROMPT}\n\n"
        f"PriceBefore product URL: {pricebefore_url}\n\n"
        "Extract only historical prices for this exact product."
        "Do not invent or estimate missing values."
    )

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            congfig=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        url_context=types.UrlContext()
                    )
                ],
                response_mime_type="application/json",
                response_schema=HistoricalPriceExtraction,
                temperature=0,
            ),
        )

        if not response.text:
            raise GeminiExtractionError(
                "Gemini returned an empty response."
            )

        extracted = HistoricalPriceExtraction.model_validate_json(
            response.text
        )

        return [
            point.model_dump()
            for point in extracted.historical_prices
        ]


    except GeminiExtractionError:
        raise