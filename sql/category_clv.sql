SELECT 
    product_category,
    COUNT(DISTINCT user_id) AS active_users,
    COUNT(transaction_id) AS total_orders,
    SUM(amount_usd) AS total_revenue,
    ROUND(AVG(amount_usd), 2) AS aov_usd,
    ROUND(SUM(amount_usd) / COUNT(DISTINCT user_id), 2) AS clv_per_user_usd
FROM transactions
GROUP BY product_category
ORDER BY total_revenue DESC;