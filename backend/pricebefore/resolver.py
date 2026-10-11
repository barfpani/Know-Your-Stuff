from urllib.parse import urlencode, urlparse

import httpx

PRICEBEFORE_BASE_URL = "https://www.pricebefore.com"

SUPPORTED_DOMAINS = {
    "amazon.in",
    "www.amazon.in",
    "flipkart.com",
    "www.flipkart.com",
    "pricebefore.com",
    "www.pricebefore.com",
}

class PriceBeforeResolutionError(Exception):
    """Raised when a product cannot be resolved on PriceBefore."""

def validate_product_url(product_url: str) -> str:
    """Validate and normalize a supported ecommerce product URL."""

    parsed_url = urlparse(product_url.strip())

    print(f"Detected hostname: {parsed_url.hostname}")

    if parsed_url.scheme != "https":
        raise ValueError("Product URL must use HTTPS.")

    if parsed_url.hostname not in SUPPORTED_DOMAINS:
        raise ValueError("Unsupported ecommerce website.")

    if not parsed_url.path or parsed_url.path == "/":
        raise ValueError("URL does not appear to be a product page.")

    return parsed_url.geturl()

async def resolver_pricebefore_url(product_url: str) -> str:
    """
    Resolve an Amazon/Flipkart URL to its PriceBefore product page.
    
    Returns:
        The final PriceBefore product URL.
        
    Raises:
        ValueError: If the input URL is invalid pr unsupported.
        PriceBeforeResolutionError: If resolution fails.
    """

    product_url = validate_product_url(product_url)

    search_url = (
        f"{PRICEBEFORE_BASE_URL}/search/"
        f"?{urlencode({'q': product_url})}"
    )

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=12.5,
            max_redirects=5,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Chrome/130.0.0.0 Safari/537.36"
                )
            },
        ) as client:
            response = await client.get(search_url)
            response.raise_for_status()

    except httpx.HTTPError as exc:
        raise PriceBeforeResolutionError(
            "Could not reach PriceBefore or resolve the product. "
        ) from exc 

    final_url = str(response.url)
    final_parsed = urlparse(final_url)

    # Ensuring the redirect stayed on PriceBefore.
    if final_parsed.hostname not in {
        "pricebefore.com",
        "www.pricebefore.com",
    }:
        raise PriceBeforeResolutionError(
            "PriceBefore redirected to an unexpected domain."
        )

    # Product pages observed so far end with a  unique ID such as
    # -917835.html. A homepage or generic page is not a match.
    if not final_parsed.path.endswith(".html"):
        raise PriceBeforeResolutionError(
            "PriceBefore did not return a product page."
        )

    if "-p" not in final_parsed.path:
        raise PriceBeforeResolutionError(
            "Resolved URL does not look like a PriceBefore product page."
        )

    return final_url

