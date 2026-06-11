CREATE TABLE retailers(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    domain VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMeSTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products(
    id SERIAL PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(150),
    category VARCHAR(100),
    normalised_name VARCHAR(255) NOT NULL,
    launch_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_listings (
    id SERIAL PRIMARY KEY,
    product_id INTERGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    retailer_id INTERGER NOT NULL REFERENCES retailers(id) ON DELETE CASCADE,
    product_url TEXT NOT NULL,
    retailer_sku VARCHAR(150),
    listing_title VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE price_history(
    id SERIAL PRIMARY KEY,
    product_listing_id INTEGER NOT NULL REFERENCES product_listing(id) ON DELETE CASCADE,
    price NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    in_stock BOOLEAN DEFAULT TIME,
    source_type VARCHAR(50) DEFAULT 'scraper',
    captured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_launch_event(
    id SERIAL PRIMARY KEY.
    brand VARCHAR(100) NOT NULL,
    product_line VARCHAR(100) NOT NULL,
    model_name VARCHAR(150) NOT NULL,
    launch_date DATE NOT NULL,
    successor_to_product_id INTEGER REFERENCES products(id) ON DELETE SET NULL
);

CREATE TABLE recommendation_logs(
    id SERIAL PRIMARY KEY,.
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    current_listing_id INTEGER REFERENCES product_listing(id) ON DELETE SET NULL,
    recommendation_type VARCHAR(50) NOT NULL,
    reason_summary TEXT NOT NULL,
    confidence_score NUMERIC(5,2),
    generate_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_listing_product_id ON product_listing(product_id);
CREATE INDEX idx_product_listing_retailer_id ON product_listing(retailer_id);
CREATE INDEX idx_pice_history_listing_id ON price_history(product_listing_id);
CREATE INDEX idx_price_history_captured_at ON price_history(captured_id);
CREATE INDEX idx_sales_events_date ON sale_events(start_date, end date);