import argparse
import logging
import random
import sys
import time

import requests

from scraper.parser.flipkart_parser import BlockedError, ParseError, parse_flipkart_product
from scraper.storage.save_prices import (
    get_connection,
    get_listing_by_url,
    save_price_snapshot,
)

logger = logging.getLogger(__name__)

# A small pool of realistic desktop User-Agents to rotate through, so every
# request doesn't share one exact fingerprint.
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]

REQUEST_TIMEOUT = 20
MAX_RETRIES = 3
BASE_BACKOFF_SECONDS = 2


def _headers() -> dict:
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-IN,en;q=0.9",
    }


def fetch_product_html(product_url: str) -> str:
    last_exc = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                product_url, headers=_headers(), timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            last_exc = exc
            if attempt == MAX_RETRIES:
                break
            sleep_for = BASE_BACKOFF_SECONDS * (2 ** (attempt - 1))
            sleep_for += random.uniform(0, 1)  # jitter
            logger.warning(
                "Fetch attempt %d/%d failed (%s); retrying in %.1fs",
                attempt,
                MAX_RETRIES,
                exc,
                sleep_for,
            )
            time.sleep(sleep_for)

    raise RuntimeError(
        f"Failed to fetch {product_url} after {MAX_RETRIES} attempts"
    ) from last_exc


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
        "price": parsed["price"],
        "in_stock": parsed["in_stock"],
    }


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    parser = argparse.ArgumentParser(description="Scrape a Flipkart product page")
    parser.add_argument("product_url", help="Flipkart product URL to scrape")
    args = parser.parse_args()

    try:
        result = scrape_flipkart_listing(args.product_url)
    except BlockedError as exc:
        print(f"Blocked/CAPTCHA detected: {exc}", file=sys.stderr)
        sys.exit(2)
    except ParseError as exc:
        print(f"Could not parse product page: {exc}", file=sys.stderr)
        sys.exit(3)
    except ValueError as exc:
        # e.g. listing not found in DB
        print(str(exc), file=sys.stderr)
        sys.exit(4)
    except RuntimeError as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        sys.exit(5)

    if result["in_stock"]:
        print(
            f"Saved snapshot {result['snapshot_id']} for listing {result['listing_id']} "
            f"({result['listing_title']}) at INR {result['price']}"
        )
    else:
        print(
            f"Saved snapshot {result['snapshot_id']} for listing {result['listing_id']} "
            f"({result['listing_title']}) - currently OUT OF STOCK"
        )


if __name__ == "__main__":
    main()