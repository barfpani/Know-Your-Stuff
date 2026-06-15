const API_URL = "http://127.0.0.1:8000/api/product/demo";

let priceChart;

function formatPrice(value) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
    }).format(value);
}

function updateRecommendation(action, message) {
    const badge = document.getElementById("recommendation-badge");
    const text = document.getElementById("recommendation-text");

    badge.textContent = action;
    badge.classList.remove("buy", "wait");
    badge.classList.add(action === "BUY" ? "buy" : "wait");

    text.textContent = message;
}

function renderChart(priceHistory) {
    const ctx = document.getElementById("priceChart");

    if (priceChart) {
        priceChart.destroy();
    }

    priceChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: priceHistory.map((point) => point.label),
            datasets: [
                {
                    label: "Price",
                    data: priceHistory.map((point) => point.price),
                    borderWidth: 2,
                    tension: 0.3,
                    borderColor: "#00d26a",
                    backgroundColor: "rgba(0, 210, 106, 0.15)",
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
            },
        },
    });
}

async function loadProductData() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const data = await response.json();

        document.getElementById("product-name").textContent = data.product_name;
        document.getElementById("current-price").textContent = formatPrice(data.current_price);
        document.getElementById("lowest-price").textContent = formatPrice(data.lowest_price);
        document.getElementById("highest-price").textContent = formatPrice(data.highest_price);
        document.getElementById("last-updated").textContent = data.last_updated;

        updateRecommendation(
            data.recommendation.action,
            data.recommendation.message
        );

        renderChart(data.price_history);
    } catch (error) {
        console.error(error);
        document.getElementById("product-name").textContent = "Unable to load product";
        document.getElementById("recommendation-text").textContent =
            "Could not fetch data from the backend. Make sure the FastAPI server is running.";
    }
}

loadProductData();