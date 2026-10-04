from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

class Product(BaseModel):
    title: str = Field(min_length=1)
    price: float = Field(ge=0)
    availability: Literal[
        "IN_STOCK",
        "OUT_OF_STOCK",
        "UNKNOWN"
    ]
    url: HttpUrl
    source: str = Field(min_length=1)

class PricePoint(BaseModel):
    date: date
    price: float = Field(ge=0)

class priceHistory(BaseModel):
    historical_prices: list[PricePoint] = Field(min_length=1)

    lowest_price: float = Field(ge=0)
    highest_price: float = Field(ge=0)

class Recommendation(BaseModel):
    decision: Literal[
        "BUY",
        "WAIT"
    ]

    source: float = Field(
        ge=0,
        le=100
    )

    reason: str = Field(min_length=1)

class ProductAnalysis(BaseModel):
    product: Product
    price_history: priceHistory
    recommendation: Recommendation