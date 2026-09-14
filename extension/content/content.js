

import { parseFlipkartProduct } from "./parsers/Flipkart.js";


// detect website and call the appropriate parser

function detectWebsite() {
    
    const hostname = window.location.hostname;

    if(hostname.includes("flipkart.com")) {
        return "flipkart";
    }

    return null;
}

// Parse current page

function parseCurrentPage(){

    const website = detectWebsite();

    if(!website) {
        console.log("Know your stuff: Unsupported website");
        return null;
    }

    switch (website) {
        
        case "flipkart":
            return parseFlipkartProduct();

        default:
            return null;

    }
}

let currentProductData = null;

//Extracting product when the content script loads

currentProductData = parseCurrentPage();

console.log(
    "Know Your Stuff - Detected:",
    currentProductData
);

//Listening for popup requests

chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if(message.type === "GET_PRODUCT_DATA") {

            sendResponse(currentProductData);
        }
    }
);

