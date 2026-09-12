

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

// send product data

function sendProductData(){

    const productData = parseCurrentPage();

    if(!productData) {
        return;
    }

    console.log("Know your stuff - Product Data:", productData);

    chrome.runtime.sendMessage({
        type: "PRODUCT_DATA",
        data: productData
    });
}

//initialize

sendProductData();