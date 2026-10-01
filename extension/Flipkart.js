function parseFlipkartProduct() {

    console.log("=== FLIPKART PARSER START ===");

    // Title

    const titleElement = document.querySelector("h1");

    const rawTitle = titleElement?.innerText?.trim() || null;

    console.log("Raw title:", rawTitle);

    // Price

    const priceElement = document.querySelector(
        "div.v1zwn21n.v1zwn20._1psv1zeb9._1psv1ze0"
    );

    const rawPrice = priceElement?.innerText?.trim() || null;

    console.log("Raw price:", rawPrice);

    // convert price to number
    
    const parsedPrice = parsePrice(rawPrice);

    console.log("Parsed price:", parsedPrice);


    //Return raw data

    const product = {
        title: rawTitle,
        price: parsedPrice,
        availability: availability || "UNKNOWN",
        url: window.location.href,
        source: "Flipkart"
    };

    console.log("Before normalization:", product);

    //Normalize 

    const normalizedProduct = normalizeProduct(product);

    console.log("After normalization:", normalizedProduct);

    console.log("Product URL:", normalizedProduct.url);

    return normalizedProduct;
}

// Availability

function getAvailability(){

    const pageText = document.body.innerText.toLowerCase();

    const hasOutofStock = pageText.includes("out of stock");

    const hasNotifyMe = pageText.includes("notify me");

    const hasBuyNow = pageText.includes("buy now");

    console.log("Out of stock text: ", hasOutofStock);
    console.log("Notify me: ", hasNotifyMe);
    console.log("Buy now: ", hasBuyNow);

    // product is actually unavailable
    if(hasOutofStock && hasNotifyMe){
        return "OUT_OF_STOCK";
    }

    // It is purchasable
    if(hasBuyNow){
        return "IN_STOCK";
    }

    return "UNKNOWN";
}

    const availability = getAvailability();

    console.log("Availability:", availability);


// Find button

function findButton(text){
    
    const elements = document.querySelectorAll(
        "button, div"
    );

    for(const element of elements){

        const elementText = element.innerText?.trim().toLowerCase();

        if(elementText === text) {
            return element;
        }
    }

    return null;
}