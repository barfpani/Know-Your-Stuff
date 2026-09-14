let produceData = null;

//Format price

function formatPrice(value) {
    
    if(value === null || value === undefined) {
        return "N/A";
    }

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
    }).format(value);
}

//Display Product

function displayProduct(data) {

    productData = data;

    document.getElementById("product-name").textContent =
        data.title || "Unknown Product";

    document.getElementById("current-price").textContent = 
        formatPrice(data.price);

    document.getElementById("last-updated").textContent =
        "Just Now";

    // Prototype will not have these

    document.getElementById("lowest-price").textContent =
        "N/A";

    document.getElementById("highest-price").textContent =
        "N/A";

    document.getElementById("recommnedation-badge").textContent =
        "TEST";

    document.getElementById("confidence-score").textContent =
        "N/A";

    document.getElementById("recommendation-text").textContent =
        `Product detected successfully from ${data.source}.`;

    console.log("Know Your Stuff - Popup received:", data);
}

//Fetching active tab data

async function loadProductData() {

    try{

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if(!tab?.id) {
            throw new Error("No active tab found");
        }

        chrome.tabs.sendMessage(
            tab.id,
            {
                type: "GET_PRODUCT_DATA"
            },
            (response) => {

                if(chrome.runtime.lastError){

                    console.error(
                        chrome.runtime.lastError.message
                    );

                    showError();
                    return;
                }

                if(!response) {
                    showError();
                    return;
                }

                displayProduct(response);
            }
        );
    }
    catch (error) {
        console.error(error);
        showError();
    }
}

//Error State

function showError() {

    document.getElementById("product-name").textContent = 
        "No Product detected";

    document.getElementById("current-price").textContent = 
        "N/A";

    document.getElementById("recommendation-text").textContent = 
        "Open a supported Flipkart product page and try again.";
}

//starting point

loadProductData();