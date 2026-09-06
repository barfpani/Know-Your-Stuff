import os
from psycopg import connect

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://barfpani@localhost:5432/know_your_stuff"
)

conn = connect(DATABASE_URL)
cur = conn.cursor()

# Check all listings
cur.execute("SELECT id, product_url FROM product_listings LIMIT 10")
rows = cur.fetchall()
print("=== All Product Listings ===")
for r in rows:
    print(f"  id={r[0]}, url={r[1]}")

# Check price history
cur.execute("SELECT id, product_listing_id, price, captured_at FROM price_history ORDER BY captured_at DESC LIMIT 10")
price_rows = cur.fetchall()
print("\n=== Recent Price History ===")
for r in price_rows:
    print(f"  listing_id={r[1]}, price={r[2]}, captured_at={r[3]}")

cur.close()
conn.close()
