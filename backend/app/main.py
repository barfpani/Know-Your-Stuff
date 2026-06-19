from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.connection import get_connection

app = FastAPI(title="Know Your Stuff API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                #this will be tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/product/{product_id}")
def get_product_data(product_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    p.id,
                    p.name AS product_name,
                    pl.id AS listing_id,
                    pl.listing_title,
                    pl.product_url,
                    r.name AS retailer_name
                FROM products p
                JOIN product_listings pl
                    ON pl.product_id = p.id
                JOIN retailers r
                    ON r.id = pl.retailer_id
                WHERE p.id = %s
                LIMIT 1
                """,
                (product_id,),
            )
            product = cur.fetchone()

            if not product:
                raise HTTPException(status_code=404, detail = "Product not found")

            cur.execute(
                """
                SELECT price, captured_at
                FROM price_history
                WHERE product_listing_id = %s
                ORDER BY captured_at ASC
                """,
                (product["listing_id"],),
            )

            price_rows = cur.fetchall()

            if not price_rows:
                raise HTTPException(status_code = 404, detail = "No price history found")

            cur.execute(
                """
                SELECT recommendation_type, reason_summary, confidence_score
                FROM recommendation_logs
                WHERE product_id = %s
                ORDER BY generated_at DESC
                LIMIT 1
                """,
                (product_id,),
            )
            
            recommendation = cur.fetchone()
    
    prices = [float(row["price"]) for row in price_rows]
    labels = [row["captured_at"].strftime("%b %d") for row in price_rows]

    response = {
        "product_name": product["product_name"],
        "retailer_name": product["retailer_name"],
        "current_price": prices[-1],
        "lowest_price": min(prices),
        "highest_price": max(prices),
        "price_history": [
            {"label": labels[i], "price": prices[i]}
            for i in range(len(prices))
        ],
        "recommendation": {
            "action": recommendation["recommendation_type"] if recommendation else "HOLD",
            "message": recommendation["reason_summary"] if recommendation else "No recommendation available yet.",
            "confidence_score": float(recommendation["confidence_score"]) if recommendation and recommendation["confidence_score"] is not None else None,
        },
        "last_updated": price_rows[-1]["captured_at"].strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    return response
