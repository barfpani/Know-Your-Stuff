import os
from decimal import Decimal

from psycopg import connect


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://barfpani@localhost:5432/know_your_stuff",
)


def get_connection():
    return connect(DATABASE_URL)


def get_listing_by_url(conn, product_url: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, product_id, retailer_id, product_url, listing_title
            FROM product_listings
            WHERE product_url = %s
            LIMIT 1
            """,
            (product_url,),
        )
        row = cur.fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "product_id": row[1],
        "retailer_id": row[2],
        "product_url": row[3],
        "listing_title": row[4],
    }


def save_price_snapshot(
    conn,
    listing_id: int,
    price: Decimal,
    *,
    currency: str = "INR",
    in_stock: bool = True,
    source_type: str = "scraper",
):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO price_history (
                product_listing_id,
                price,
                currency,
                in_stock,
                source_type
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (listing_id, price, currency, in_stock, source_type),
        )
        snapshot_id = cur.fetchone()[0]

    conn.commit()
    return snapshot_id
