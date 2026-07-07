import re
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup


PRICE_PATTERN = re.compile(r"[\d,]+(?:\.\d+)?")


def _clean_price(text: str) -> Decimal:
    match = PRICE_PATTERN.search(text.replace("\u20b9", "").replace("Rs.", ""))
    if not match:
        raise ValueError("Could not find a numeric price in the provided text")

    normalized = match.group(0).replace(",", "")

    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid price value: {text}") from exc


def parse_flipkart_product(html: str):
    soup = BeautifulSoup(html, "lxml")

    title = None
    for selector in ("span.B_NuCI", "h1._6EBuvT span", "h1 span"):
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            title = element.get_text(strip=True)
            break

    price = None
    for selector in ("div._30jeq3._16Jk6d", "div.Nx9bqj.CxhGGd", "div._30jeq3"):
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            price = _clean_price(element.get_text(strip=True))
            break

    if not title:
        raise ValueError("Could not parse Flipkart product title")

    if price is None:
        raise ValueError("Could not parse Flipkart product price")

    return {
        "listing_title": title,
        "price": price,
        "currency": "INR",
        "in_stock": True,
    }
