// console.log("Know Your Stuff: content.js LOADED");


// Detect website and call the appropriate parser

function detectWebsite() {

    const hostname = window.location.hostname;

    if (hostname.includes("flipkart.com")) {
        return "flipkart";
    }

    return null;
}


// Parse current page

function parseCurrentPage() {

    const website = detectWebsite();

    if (!website) {
        console.log("Know Your Stuff: Unsupported website");
        return null;
    }

    switch (website) {

        case "flipkart":
            return parseFlipkartProduct();

        default:
            return null;
    }
}


// Extract product when the content script loads

const currentProductData = parseCurrentPage();

console.log(
    "Know Your Stuff - Detected:",
    currentProductData
);


// Listen for popup requests

chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (message.type === "GET_PRODUCT_DATA") {
            sendResponse(currentProductData);
        }

    }
);