

export function parsePrice(priceText) {
    
    if(!priceText){
        return null;
    }

    /*
    examples:
    - "₹1,299"
    - "₹ 1,299"
    - "Rs. 1,299"
     */

    const cleaned = priceText
        .replace(/[₹＄€￡]/g,"")
        .replace(/,/g,"")
        .replace(/[^\d.]/g,"")
        .trim();

    if(!cleaned){
        return null;
    }

    const price = Number.parseFloat(cleaned);

    return Number.isNaN(price) ? null : price;
}

