// Format Price

function formatPrice(value) {

    if(value === null || value === undefined){
        return "N/A";
    }

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0
    }).format(value);                                                        
}

// Display product data

function displayProduct(data) {
    if(!data) {
        showError("No product data received.");
        return;
    }

    console.log("Know your stuff - Product received:", data)

    // Product name

    document.getElementById("product-name").textContent = data.title || "Unknown Product";

    // current price

    document.getElementById("current-price").textContent = formatPrice(data.price);

    // Availability 

    document.getElementById("availability").textContent = data.availability || "UNKNOWN";

    // status

    document.getElementById("status-text").textContent = "Product detected succesfully.";

    // URL

    document.getElementById("product-url").textContent = data.url || "N/A";

    // Last updated 

    document.getElementById("last-updated").textContent = "just now";

}

// Error state

function showError(message) {


    console.error("Know Your Stuff:", message);

    document.getElementById("Product-name").textContent = "No product detected";

    document.getElementById("current-price").textContent = "N/A";

    document.getElementById("Availability").textContent = "N/A";

    document.getElementById("source").textContent = "N/A";

    document.getElementById("product-url").textContent = "N/A";

    document.getElementById("status-text").textContent = message;

}

// Request product data

async function loadProductData() {

    try {
        
        console.log("Know Your Stuff: Requesting product data...");

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if(!tab || !tab.id) {
            showError("Could not find the active tab.");
            return;
        }

        console.log("Active tab:", tab.url);

        chrome.tabs.sendMessage(
            tab.id,
            {
                type:"GET_PRODUCT_DATA"
            },
            (response) => {
                
                //checking for messaging errors

                if(chrome.runtime.lastError) {

                    console.error(
                        "Message error:",
                        chrome.runtime.lastError.message
                    );

                    showError("Could not connect to the product page.");

                    return;
                }

                console.log("response from content.js", response);

                displayProduct(response);
            }
        );
    }
    catch (error) {
        console.error("Failed to load product data:", error);

        showError(
            "Failed to load product data."
        );
    }
}

// Start

loadProductData();