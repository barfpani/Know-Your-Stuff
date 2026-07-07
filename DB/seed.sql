INSERT INTO retailers (name, domain)
VALUES 
    ('Flipkart', 'flipkart.com'),
    ('Amazon', 'amazon.in'),
    ('Croma', 'croma.com'),
    ('VijaySales', 'vijaysales.com');

Insert INTO products (brand, name, model, category, normalised_name, launch_date)
VALUES
    ('Samsung', 'Samsung Galaxy S25 Ultra', 'S25 Ultra', 'Smartphone', 'samsung-galaxy-s25-ultra', '2025-01-20');


INSERT INTO product_listings(product_id, retailer_id, product_url, retailer_sku, listing_title)
VALUES
    (1, 1, 'http://www.flipkart.com/sample-s25-ultra', 'FK-S25U-001', 'Samsung Galaxy S25 Ultra'),
    (1, 2, 'http://www.amazon.in/sample-s25-ultra', 'AMZ-S25U-001', 'Samsung Galaxy S25 Ultra');

INSERT INTO price_history (product_listing_id, price, currency, in_stock, source_type, captu red_at)
VALUES
    (1, 129999, 'INR', TRUE, 'scraper', '2025-01-25 10:00:00'),
    (1, 119999, 'INR', TRUE, 'scraper', '2025-02-22 10:00:00'),
    (1, 109999, 'INR', TRUE, 'scraper', '2025-03-31 10:00:00'),
    (1, 139999, 'INR', TRUE, 'scraper', '2025-05-05 10:00:00'),
    (1, 99999, 'INR', TRUE, 'scraper', '2025-06-23 10:00:00'),
    (1, 129999, 'INR', TRUE, 'scraper', '2025-07-22 10:00:00');
    

INSERT INTO sales_events (name, retailer_id, start_date, end_date, description)
VALUES
    ('Big Billion Days', 1, '2026-10-1', '2026-10-10', 'Expected major Flipkart discount event');

INSERT INTO recommendation_logs (product_id, current_listing_id, recommendation_type, reason_summary, confidence_score)
VALUES
    (1, 1, 'BUY', 'Big Billion Days is approaching and the product has historically dropped during major sales events', 87.50);