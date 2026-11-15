import asyncio
import json

from backend.gemini.gemini import (
    GeminiExtractionError,
    analyse_product_with_gemini,
)
from backend.schema.product_schema import Product


PRODUCT = Product(
    title="Sony WF-C710N Noise Cancellation Earbuds with AI Reduction, Clear Calls, TWS Bluetooth",
    price=6989.0,
    availability="IN_STOCK",
    url=(
        "https://www.flipkart.com/"
        "sony-wf-c710n-noise-cancellation-earbuds-ai-reduction-clear-calls-tws-bluetooth/p/itm8cb44c771a7f0?pid=ACCHCV3USTHM8BJA&lid=LSTACCHCV3USTHM8BJAMPE0UC&marketplace=FLIPKART&q=sony+wf+c710n&store=0pm%2Ffcn%2F821%2Fa7x%2F2si&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_ps&fm=search-autosuggest&iid=fa028e65-2f4f-4c4e-b510-10df266f8ba5.ACCHCV3USTHM8BJA.SEARCH&ppt=sp&ppn=sp&ssid=b2zx25bg2o0000001792411928236&qH=b1fa7234bb900df5&ov_redirect=true&ov_redirect=true"
    ),
    source="Flipkart",
)

PRICEBEFORE_URL = (
    "https://www.pricebefore.com/sony-wf-c710n-lzin-bluetooth-p917835.html"
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
