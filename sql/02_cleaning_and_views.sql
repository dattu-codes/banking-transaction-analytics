
-- Clean raw records while retaining quality flags.
DROP TABLE IF EXISTS cleaned_transactions;

CREATE TABLE cleaned_transactions AS
WITH ranked_transactions AS (
    SELECT *,
        UPPER(TRIM(status)) AS standardized_status,
        ROW_NUMBER() OVER (
            PARTITION BY transaction_id
            ORDER BY transaction_id
        ) AS row_num
    FROM raw_transactions
)
SELECT
    transaction_id,
    customer_id,
    transaction_date,
    transaction_type,
    CASE WHEN amount > 0 THEN amount ELSE NULL END AS amount,
    currency,
    channel,
    standardized_status AS status,
    merchant_category,
    country,
    CASE
        WHEN amount IS NULL THEN 'MISSING'
        WHEN amount <= 0 THEN 'NON_POSITIVE'
        ELSE 'VALID'
    END AS amount_quality,
    CASE
        WHEN customer_id IS NULL
             OR TRIM(customer_id) = ''
        THEN 'MISSING'
        ELSE 'VALID'
    END AS customer_id_quality
FROM ranked_transactions
WHERE row_num = 1;

-- Monthly transaction summary.
CREATE OR REPLACE VIEW vw_monthly_transaction_summary AS
SELECT
    DATE_TRUNC('month', transaction_date)::DATE AS transaction_month,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE status = 'SUCCESS') AS successful_transactions,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'SUCCESS')
        / NULLIF(COUNT(*), 0), 2
    ) AS success_rate_pct,
    COALESCE(
        SUM(amount) FILTER (WHERE status = 'SUCCESS'), 0
    ) AS successful_amount_inr,
    COUNT(*) FILTER (WHERE amount_quality <> 'VALID')
        AS amount_quality_issues,
    COUNT(*) FILTER (WHERE customer_id_quality = 'MISSING')
        AS missing_customer_id_count
FROM cleaned_transactions
GROUP BY DATE_TRUNC('month', transaction_date)::DATE;

-- Channel performance summary.
CREATE OR REPLACE VIEW vw_channel_summary AS
SELECT
    channel,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE status = 'SUCCESS') AS successful,
    COUNT(*) FILTER (WHERE status = 'FAILED') AS failed,
    COUNT(*) FILTER (WHERE status = 'PENDING') AS pending,
    COUNT(*) FILTER (WHERE status = 'REVERSED') AS reversed,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'SUCCESS')
        / NULLIF(COUNT(*), 0), 2
    ) AS success_rate_pct,
    COALESCE(
        SUM(amount) FILTER (WHERE status = 'SUCCESS'), 0
    ) AS successful_amount_inr,
    COUNT(*) FILTER (WHERE amount_quality <> 'VALID')
        AS amount_quality_issues
FROM cleaned_transactions
GROUP BY channel;

-- Transaction status distribution.
CREATE OR REPLACE VIEW vw_status_summary AS
SELECT
    status,
    COUNT(*) AS transaction_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2
    ) AS percentage_of_transactions
FROM cleaned_transactions
GROUP BY status;

-- Data quality reconciliation summary.
CREATE OR REPLACE VIEW vw_data_quality_summary AS
SELECT 'Rows in raw table' AS metric,
       COUNT(*)::BIGINT AS metric_value
FROM raw_transactions

UNION ALL
SELECT 'Rows in cleaned table', COUNT(*)::BIGINT
FROM cleaned_transactions

UNION ALL
SELECT 'Duplicate rows removed',
       ((SELECT COUNT(*) FROM raw_transactions)
        - (SELECT COUNT(*) FROM cleaned_transactions))::BIGINT

UNION ALL
SELECT 'Missing customer IDs', COUNT(*)::BIGINT
FROM cleaned_transactions
WHERE customer_id_quality = 'MISSING'

UNION ALL
SELECT 'Missing amounts', COUNT(*)::BIGINT
FROM cleaned_transactions
WHERE amount_quality = 'MISSING'

UNION ALL
SELECT 'Zero or negative amounts', COUNT(*)::BIGINT
FROM cleaned_transactions
WHERE amount_quality = 'NON_POSITIVE'

UNION ALL
SELECT 'Nonstandard statuses', COUNT(*)::BIGINT
FROM cleaned_transactions
WHERE status NOT IN ('SUCCESS', 'FAILED', 'PENDING', 'REVERSED');
