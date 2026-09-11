import { parsePrice } from '../utils/priceParser.js';
import { normalizeProduct } from "../../utils/priceNormalizer.js";

export function parseFlipkartProduct() {
    const rawFile = getProductTitle();
    const rawPrice = getProductPrice();
    const rawAvailability = getAvailability();

    const product = {
        title: rawTitle,
        price: parsePrice(rawPrice),
        availability: rawAvailability,
        url: window.location.href,
        source: "Flipkart"
    };

    return normalizeProduct(product);
}

function getProductTitle(){
    
    const selectors = [
        "span.B_NuCI",
        "h1._6EBuvT",
        "h1",
        "[Class*='product-title']"
    ];

    for(const selector of selectors){
        const element = document.querySelector(selector);

        if(element?.innerText?.trim()) {
            return element.innerText.trim();
        }
    }

    return null;
}

function getProductPrice(){

    const selectors = [
        "div.Nx9bqj",
        "div._30jeq3",
        "[class*='Nx9bj']",
        "[class*='price']"
    ];

    for (const selector of selectors){
        const element = document.querySelector(selector);

        if(element?.innerText?.trim()){
            return element.innerText.trim();
        }
    }

    return null;
}

function getAvailability() {

    const selectors = [
        "#availability",
        "[class*='availability']",
        "class*='Availability']"
    ];

    for (const selector of selectors){
            
        const element = document.querySelector(selector);

        if(element?.innerText?.trim()){
            return element.innerText.trim();
        }
    }


    //Flipkart often doesn't have a dedicated availability element.
    //If the product page exists and has a price, we can initially 
    // treat it as available.

    const priceElement = document.querySelector(
        "div.Nx9bqj, div._30jeq3"
    );

    if(priceElement) {
        return "Available";
    }

    return "Unknown";
}