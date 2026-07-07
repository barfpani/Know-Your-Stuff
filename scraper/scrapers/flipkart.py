import argparse

import requests

from scraper.parser.flipkart_parser import parse_flipkart_product
from scraper.storage.save_prices import (
    get_connection,
    get_listing_by_url,
    save_price_snapshot,
)


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}


def fetch_product_html(product_url: str) -> str:
    response = requests.get(product_url, headers=DEFAULT_HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def scrape_flipkart_listing(product_url: str):
    html = fetch_product_html(product_url)
    parsed = parse_flipkart_product(html)

    with get_connection() as conn:
        listing = get_listing_by_url(conn, product_url)
        if not listing:
            raise ValueError(
                "No product_listings row found for this URL. "
                "Insert the listing first, then scrape it."
            )

        snapshot_id = save_price_snapshot(
            conn,
            listing["id"],
            parsed["price"],
            currency=parsed["currency"],
            in_stock=parsed["in_stock"],
            source_type="scraper",
        )

    return {
        "snapshot_id": snapshot_id,
        "listing_id": listing["id"],
        "listing_title": parsed["listing_title"],
        "price": str(parsed["price"]),
    }


def main():
    parser = argparse.ArgumentParser(description="Scrape a Flipkart product page")
    parser.add_argument("product_url", help="Flipkart product URL to scrape")
    args = parser.parse_args()

    result = scrape_flipkart_listing(args.product_url)
    print(
        f"Saved snapshot {result['snapshot_id']} for listing {result['listing_id']} "
        f"({result['listing_title']}) at INR {result['price']}"
    )


if __name__ == "__main__":
    main()
