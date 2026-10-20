import asyncio 

from backend.gemini.gemini import extract_price_history


async def main():
    url = (
        "https://www.pricebefore.com/"
        "skullcandy-crusher-evo-40mm-drivers-40hr-p918702.html"
    )

    history = await extract_price_history(url)

    for point in history:
        print(point)

if __name__ == "__main__":
    asyncio.run(main())