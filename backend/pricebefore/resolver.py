from urllib.parse import urlencode, urlparse

from playwright.async_api import async_playwright, Error as PlaywrightError

PRICEBEFORE_BASE_URL = "https://www.pricebefore.com"

SUPPORTED_DOMAINS = {
    "amazon.in",
    "www.amazon.in",
    "flipkart.com",
    "www.flipkart.com",
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
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)

            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/130.0.0.0 Safari/537.36"
                ),
                locale="en-IN"
            )

            page = await context.new_page()

            response = await page.goto(
                search_url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            if response is None or response.status >= 400:
                status = response.status if response else "no response"
                raise PriceBeforeResolutionError(
                    f"PriceBefore returned HTTP {status}."
                )

            final_url = page.url
            await browser.close()

    except PlaywrightError as exc:
        raise PriceBeforeResolutionError(
            "Could not resolve this product through PriceBefore."
        ) from exc

    finally:
        if browser is not None:
            await browser.close()

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

