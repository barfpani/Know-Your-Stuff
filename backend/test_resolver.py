import asyncio 


from pricebefore.resolver import (
    resolver_pricebefore_url,
    PriceBeforeResolutionError,
)

async def main():
    product_url = input("Enter the Flipkart/Amazon product URL: ").strip()

    try:
        resolved_url = await resolver_pricebefore_url(product_url)

        print("\nResolution successful!")
        print("PriceBefore URL: ", resolved_url)

    except (ValueError, PriceBeforeResolutionError) as exc:
        print("\nResolution failed:", exc)

if __name__ == "__main__":
    asyncio.run(main())