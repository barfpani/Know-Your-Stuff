import logging
import re
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

PRICE_PATTERN = re.compile(r"[\d,]+(?:\.\d+)?")

# Selectors checked in order; first match wins. Flipkart's class names are
# obfuscated and rotate periodically, so keep this list easy to extend.
TITLE_SELECTORS = ("span.B_NuCI", "h1._6EBuvT span", "h1 span")
PRICE_SELECTORS = ("div._30jeq3._16Jk6d", "div.Nx9bqj.CxhGGd", "div._30jeq3")

# Phrases that indicate the product is unavailable, checked against the
# whole page text (case-insensitive).
OUT_OF_STOCK_MARKERS = (
    "sold out",
    "currently unavailable",
    "out of stock",
    "notify me",
)

# Rough signal that we got a bot-check/interstitial page instead of the
# real product page, so we can raise a distinct, actionable error.
CAPTCHA_MARKERS = (
    "captcha",
    "unusual traffic",
    "access denied",
)


class ParseError(ValueError):
    """Raised when the product page can't be parsed as expected."""


class BlockedError(ParseError):
    """Raised when the response looks like a CAPTCHA/anti-bot page."""


def _clean_price(text: str) -> Decimal:
    match = PRICE_PATTERN.search(text.replace("\u20b9", "").replace("Rs.", ""))
    if not match:
        raise ParseError("Could not find a numeric price in the provided text")

    normalized = match.group(0).replace(",", "")

    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ParseError(f"Invalid price value: {text}") from exc


def _looks_blocked(page_text_lower: str) -> bool:
    return any(marker in page_text_lower for marker in CAPTCHA_MARKERS)


def _looks_out_of_stock(soup: BeautifulSoup, page_text_lower: str) -> bool:
    # Prefer a specific "add to cart" / "buy now" button check when present;
    # fall back to scanning visible text for known out-of-stock phrasing.
    add_to_cart = soup.select_one("button._2KpZ6l._2U9uOA")
    if add_to_cart and "notify" in add_to_cart.get_text(strip=True).lower():
        return True

    return any(marker in page_text_lower for marker in OUT_OF_STOCK_MARKERS)


def parse_flipkart_product(html: str):
    soup = BeautifulSoup(html, "lxml")
    page_text_lower = soup.get_text(" ", strip=True).lower()

    if _looks_blocked(page_text_lower):
        raise BlockedError(
            "Response looks like a CAPTCHA/anti-bot page, not a product page"
        )

    title = None
    for selector in TITLE_SELECTORS:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            title = element.get_text(strip=True)
            break

    if not title:
        logger.warning(
            "Could not find title with known selectors; page may have changed. "
            "First 500 chars: %s",
            html[:500],
        )
        raise ParseError("Could not parse Flipkart product title")

    in_stock = not _looks_out_of_stock(soup, page_text_lower)

    price = None
    if in_stock:
        for selector in PRICE_SELECTORS:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                price = _clean_price(element.get_text(strip=True))
                break

        if price is None:
            logger.warning(
                "Could not find price with known selectors; page may have changed. "
                "First 500 chars: %s",
                html[:500],
            )
            raise ParseError("Could not parse Flipkart product price")

    return {
        "listing_title": title,
        "price": price,
        "currency": "INR",
        "in_stock": in_stock,
    }