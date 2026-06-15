from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Know Your Stuff API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                #this will be tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_PRODUCT = {
    "product_name": "Samsung Galaxy S25 Ultra",
    "current_price": 89999,
    "lowest_price": 69999,
    "highest_price": 129999,
    "recommendation": {
        "action": "WAIT",
        "message": (
            "Big billion days sale is approaching and this product historically dropped during major sale events."
        ),
        "confidence_score": 87.5,
    },
    "price_history": [
        {"label": "launch", "price": 129999},
        {"label": "Month 1", "price": 127999},
        {"label": "Month 2", "price": 109999},
        {"label": "Month 3", "price": 99999},
        {"label": "Month 4", "price": 69999},
        {"label": "Month 5", "price": 89999},
    ],
    "last_updated": "2025-01-25 10:10:00",
}

@app.get("/api/product/demo")
def get_demo_product():
    return DEMO_PRODUCT