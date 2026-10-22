from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.pricebefore.resolver import (
    resolver_priicebefore_url, PriceBeforeResolutionError,
)

from backend.gemini.gemini import (
    extract_price_history, GeminiExtractionError,
)

from backend.schema.product_schema import (
    Product,
    PricePoint,
    PriceHistory,
)

app = FastAPI(
    title="Know Your Stuff API",
    description="Product price history and ananlysis API",
    version="0.1.0",
)

class AnalysisResponse(BaseModel):
    product: Product
    price_history: PriceHistory


@app.get("/")
async def root():
    return {
        "message": "Know your stuff API is running",
        "version": "0.1.0",
    }

@app.post("/api/analyse", response_model=AnalysisResponse)
async def analyse_product(product: Product):
    """
    Resolve a product on PriceBefore, extract it's historical
    prices using Gemini, and calculate price statistics.
    """

    #Resolve the original product URL
    try:
        pricebefore_url = await resolver_priicebefore_url(
            str(product.url)
        )

    except PriceBeforeResolutionError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find product history: {exc}",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )from exc

    #Extract historical prices using gemini.
    try:
        history_data = await extract_price_history(
            pricebefore_url
        )

    except GeminiExtractionError as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to extract price history.",
        ) from exc

    #Validate the historical price points.
    try:
        price_points = [
            PricePoint(**point)
            for point in history_data
        ]

        #Sorting form oldest to newest.
        price_points.sort(key=lambda point: point.date)

        prices = [point.price for point in price_points]

        price_history = PriceHistory(
            historical_prices=price_points,
            lowest_price=min(prices),
            highest_price=max(prices),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Historical price data failed validation.",
        )from exc


    #Returning the validated result
    return AnalysisResponse(
        product=product,
        price_history=price_history,
    )