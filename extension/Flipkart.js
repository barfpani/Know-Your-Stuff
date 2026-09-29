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
        availability: "TEST",
        url: window.location.href,
        source: "Flipkart"
    };

    console.log("Before normalization:", product);

    //Normalize 

    const normalizedProduct = normalizeProduct(product);

    console.log("After normalization:", normalizedProduct);

    return normalizedProduct;
}