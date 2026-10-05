from schema.product_schema import PricePoint, PriceHistory


# Test 1: PricePoint
price_point = PricePoint(
    date="2026-09-01",
    price=8999
)

print("PricePoint:")
print(price_point)
print()


# Test 2: PriceHistory
price_history = PriceHistory(
    historical_prices=[
        PricePoint(
            date="2026-09-01",
            price=8999
        ),
        PricePoint(
            date="2026-09-15",
            price=8499
        ),
        PricePoint(
            date="2026-10-01",
            price=8022
        )
    ],
    lowest_price=8022,
    highest_price=8999
)

print("PriceHistory:")
print(price_history)