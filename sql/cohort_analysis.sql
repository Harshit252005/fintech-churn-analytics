WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', CAST(signup_date AS DATE)) AS cohort_month
    FROM users
),
user_activities AS (
    SELECT DISTINCT
        t.user_id,
        DATE_TRUNC('month', CAST(t.transaction_date AS DATE)) AS activity_month
    FROM transactions t
),
cohort_size AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT user_id) AS num_users
    FROM user_cohorts
    GROUP BY cohort_month
),
retention AS (
    SELECT 
        c.cohort_month,
        a.activity_month,
        -- Month offset calculation
        (EXTRACT(YEAR FROM a.activity_month) - EXTRACT(YEAR FROM c.cohort_month)) * 12 +
        (EXTRACT(MONTH FROM a.activity_month) - EXTRACT(MONTH FROM c.cohort_month)) AS month_number,
        COUNT(DISTINCT c.user_id) AS active_users
    FROM user_cohorts c
    JOIN user_activities a ON c.user_id = a.user_id
    WHERE a.activity_month >= c.cohort_month
    GROUP BY c.cohort_month, a.activity_month
)
SELECT 
    r.cohort_month,
    s.num_users AS cohort_initial_size,
    r.month_number,
    r.active_users,
    ROUND(CAST(r.active_users AS DOUBLE) / s.num_users * 100, 2) AS retention_rate_pct
FROM retention r
JOIN cohort_size s ON r.cohort_month = s.cohort_month
WHERE r.month_number <= 12
ORDER BY r.cohort_month, r.month_number;