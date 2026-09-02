WITH user_summary AS (
    SELECT 
        u.user_id,
        u.account_tier,
        u.primary_product,
        MAX(t.transaction_date) AS max_tx_date,
        COUNT(t.transaction_id) AS total_transactions,
        COALESCE(SUM(t.amount_usd), 0) AS total_monetary_value
    FROM users u
    LEFT JOIN transactions t ON u.user_id = t.user_id
    GROUP BY u.user_id, u.account_tier, u.primary_product
),
rfm_scores AS (
    SELECT 
        user_id,
        account_tier,
        primary_product,
        total_transactions,
        total_monetary_value,
        COALESCE(DATE_DIFF('day', CAST(max_tx_date AS DATE), DATE '2025-12-01'), 999) AS recency_days,
        NTILE(3) OVER (ORDER BY COALESCE(DATE_DIFF('day', CAST(max_tx_date AS DATE), DATE '2025-12-01'), 999) ASC) AS r_score,
        NTILE(3) OVER (ORDER BY total_transactions DESC) AS f_score,
        NTILE(3) OVER (ORDER BY total_monetary_value DESC) AS m_score
    FROM user_summary
)
SELECT 
    user_id,
    account_tier,
    primary_product,
    recency_days,
    total_transactions,
    total_monetary_value,
    r_score, f_score, m_score,
    CASE 
        WHEN r_score = 1 AND f_score = 1 AND m_score = 1 THEN 'VIP'
        WHEN r_score >= 2 AND m_score <= 2 THEN 'At Risk'
        ELSE 'Lost / Inactive'
    END AS rfm_segment
FROM rfm_scores;