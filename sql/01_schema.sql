
CREATE TABLE IF NOT EXISTS raw_transactions (
    transaction_id VARCHAR(20),
    customer_id VARCHAR(20),
    transaction_date DATE,
    transaction_type VARCHAR(20),
    amount NUMERIC(12, 2),
    currency VARCHAR(5),
    channel VARCHAR(30),
    status VARCHAR(30),
    merchant_category VARCHAR(30),
    country VARCHAR(30)
);
