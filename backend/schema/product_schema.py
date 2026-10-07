from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator

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

class PriceHistory(BaseModel):

    historical_prices: list[PricePoint] = Field(min_length=1)

    lowest_price: float = Field(ge=0)
    highest_price: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_price_range(self):
        prices = [
            point.price
            for point in self.historical_prices
        ]

        actual_lowest = min(prices)
        actual_highest = max(prices)

        if self.lowest_price != actual_lowest:
            raise ValueError(
                f"lowest_price must be {actual_lowest},"
                f"got {self.lowest_price}"
            )

        if self.highest_price != actual_highest:
            raise ValueError(
                f"highest price must be {actual_highest},"
                f"got {self.highest_price}"
            )

        return self
    

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
    price_history: PriceHistory
    recommendation: Recommendation