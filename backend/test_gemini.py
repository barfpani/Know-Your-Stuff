import asyncio
import json

from backend.gemini.gemini import (
    GeminiExtractionError,
    analyse_product_with_gemini,
)
from backend.schema.product_schema import Product


PRODUCT = Product(
    title="Skullcandy Crusher Evo",
    price=12999,
    availability="IN_STOCK",
    url=(
        "https://www.flipkart.com/"
        "skullcandy-crusher-evo-40mm-drivers-40hr-playtime-rapid-charge/"
        "p/itmc7c802dc62ef2"
    ),
    source="Flipkart",
)

PRICEBEFORE_URL = (
    "https://www.pricebefore.com/"
    "skullcandy-crusher-evo-40mm-drivers-40hr-p918702.html"
)


async def main():
    try:
        analysis = await analyse_product_with_gemini(
            PRODUCT,
            PRICEBEFORE_URL,
        )
    except GeminiExtractionError as exc:
        print(f"Gemini analysis failed: {exc}")

        if exc.__cause__:
            print(f"Underlying error: {exc.__cause__}")

        raise

    print(
        json.dumps(
            analysis.model_dump(),
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
