

export function normalizeProduct(product) {

    return {
        title: cleanText(product.title),
        price: product.price,
        availability: cleanText(product.availability),
        url: product.url,
        source: product.source
    };
}

function cleanText(text) {
    
    if(!text) {
        return null;
    }

    return text.replace(/\s+/g," ").trim();
}