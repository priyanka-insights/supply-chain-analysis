USE olist_supply_chain;

-- ═══════════════════════════════════════════════════════════════
-- SUPPLY CHAIN DELAY ANALYSIS — SQL BUSINESS QUERIES
-- Dataset  : Olist Brazil E-Commerce (Kaggle)
-- Table    : supply_chain
-- Queries  : 7 (Basic → Intermediate → Advanced)
-- ═══════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════════
-- QUERY 1: OVERALL BUSINESS HEALTH SUMMARY          [Basic]
-- Purpose : Single query to get a full health check of the
--           business — delay rate, financial loss, average
--           delay days, and review score comparison between
--           delayed and on-time orders.
-- ═══════════════════════════════════════════════════════════════

SELECT
    COUNT(*)                                    AS total_orders,
    SUM(is_delayed)                             AS delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2)             AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_delayed = 1
              THEN delay_days END), 1)          AS avg_delay_days,
    ROUND(SUM(penalty_cost), 2)                 AS total_penalty_cost,
    ROUND(AVG(CASE WHEN is_delayed = 1
              THEN review_score END), 2)        AS avg_review_delayed,
    ROUND(AVG(CASE WHEN is_delayed = 0
              THEN review_score END), 2)        AS avg_review_ontime
FROM supply_chain;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 2: STATE-WISE DELAY RANKING                 [Basic]
-- Purpose : Identify which customer states have the worst
--           delay problem. Shows both delay rate (%) and
--           absolute volume so we can distinguish between
--           high-rate small states vs high-volume large states.
-- ═══════════════════════════════════════════════════════════════

SELECT
    customer_state,
    COUNT(*)                                AS total_orders,
    SUM(is_delayed)                         AS delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2)         AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_delayed = 1
              THEN delay_days END), 1)      AS avg_delay_days,
    ROUND(SUM(penalty_cost), 2)             AS total_penalty_cost,
    ROUND(AVG(review_score), 2)             AS avg_review_score
FROM supply_chain
GROUP BY customer_state
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 3: FESTIVE VS NORMAL SEASON COMPARISON      [Intermediate]
-- Purpose : Determine whether the Nov-Dec festive/peak season
--           causes significantly more delays than the rest of
--           the year. Uses CASE WHEN to split orders into two
--           seasonal groups and compares delay rate and review
--           score between them.
-- ═══════════════════════════════════════════════════════════════

SELECT
    CASE WHEN is_festive = 1
         THEN 'Festive Season'
         ELSE 'Normal Season'
    END                                     AS season_type,
    COUNT(*)                                AS total_orders,
    SUM(is_delayed)                         AS delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2)         AS delay_rate_pct,
    ROUND(AVG(CASE WHEN is_delayed = 1
              THEN delay_days END), 1)      AS avg_delay_days,
    ROUND(AVG(review_score), 2)             AS avg_review_score,
    ROUND(SUM(penalty_cost), 2)             AS total_penalty_cost
FROM supply_chain
GROUP BY is_festive
ORDER BY is_festive DESC;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 4: MONTHLY TREND ANALYSIS                   [Intermediate]
-- Purpose : Track delay rate and penalty cost month by month
--           across all years to identify seasonal patterns and
--           determine whether the situation is improving or
--           worsening over time.
-- ═══════════════════════════════════════════════════════════════

SELECT
    order_year,
    order_month,
    COUNT(*)                                AS total_orders,
    SUM(is_delayed)                         AS delayed_orders,
    ROUND(AVG(is_delayed) * 100, 2)         AS delay_rate_pct,
    ROUND(AVG(review_score), 2)             AS avg_review_score,
    ROUND(SUM(penalty_cost), 2)             AS monthly_penalty
FROM supply_chain
GROUP BY order_year, order_month
ORDER BY order_year, order_month;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 5: RUNNING CUMULATIVE DELAYS                [Advanced — Window Function]
-- Purpose : Calculate a running total of delayed orders over
--           time to see how the total delay burden accumulates
--           month by month. Uses SUM() OVER() window function
--           with ROWS UNBOUNDED PRECEDING to build the running
--           sum from the first month up to each current month.
-- Business use : Are delays piling up cumulatively, or is the
--           situation being contained month over month?
-- ═══════════════════════════════════════════════════════════════

WITH monthly_data AS (
    SELECT
        order_year,
        order_month,
        COUNT(*)                        AS total_orders,
        SUM(is_delayed)                 AS delayed_orders,
        ROUND(AVG(is_delayed)*100, 2)   AS delay_rate_pct
    FROM supply_chain
    GROUP BY order_year, order_month
)
SELECT
    order_year,
    order_month,
    total_orders,
    delayed_orders,
    delay_rate_pct,
    SUM(delayed_orders) OVER (
        ORDER BY order_year, order_month
        ROWS UNBOUNDED PRECEDING
    )                                   AS cumulative_delayed
FROM monthly_data
ORDER BY order_year, order_month;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 6: MONTH-OVER-MONTH DELAY CHANGE            [Advanced — Window Function]
-- Purpose : Calculate the percentage change in delay rate
--           from one month to the next using LAG() window
--           function. Shows whether the delay situation is
--           improving or worsening relative to the prior month.
-- Formula : (current_month_rate - prev_month_rate)
--            / prev_month_rate * 100
-- Business use : Identify which months saw the sharpest
--           deterioration or improvement in delivery performance.
-- ═══════════════════════════════════════════════════════════════

WITH monthly_data AS (
    SELECT
        order_year,
        order_month,
        COUNT(*)                        AS total_orders,
        SUM(is_delayed)                 AS delayed_orders,
        ROUND(AVG(is_delayed)*100, 2)   AS delay_rate_pct
    FROM supply_chain
    GROUP BY order_year, order_month
)
SELECT
    order_year,
    order_month,
    total_orders,
    delay_rate_pct,
    LAG(delay_rate_pct, 1) OVER (
        ORDER BY order_year, order_month
    )                                   AS prev_month_rate,
    -- Percentage change: positive = delay got worse, negative = delay improved
    ROUND(
        (delay_rate_pct - LAG(delay_rate_pct, 1) OVER (ORDER BY order_year, order_month))
        / LAG(delay_rate_pct, 1) OVER (ORDER BY order_year, order_month)
        * 100
    , 2)                                AS mom_change_pct
FROM monthly_data
ORDER BY order_year, order_month;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 7: PRIORITY CUSTOMER LIST                   [Advanced — CTE + JOIN]
-- Purpose : Identify the worst-affected customers for the
--           customer support team to prioritize. These are
--           orders where delay_days exceeds the state average
--           AND the customer gave a review score of 2 or below.
-- Step 1  : CTE calculates the average delay per state
--           (for delayed orders only).
-- Step 2  : Main query joins back to the full table and filters
--           for orders above that state average with low reviews.
-- Business use : Give the support team a ranked list of high-
--           priority customers who need proactive outreach.
-- ═══════════════════════════════════════════════════════════════

WITH state_avg AS (
    -- Step 1: Calculate average delay days per state for delayed orders only
    SELECT
        customer_state,
        ROUND(AVG(delay_days), 1)   AS state_avg_delay
    FROM supply_chain
    WHERE is_delayed = 1
    GROUP BY customer_state
)
SELECT
    s.order_id,
    s.customer_state,
    s.delay_days,
    sa.state_avg_delay,
    ROUND(s.delay_days - sa.state_avg_delay, 1) AS above_avg_by,
    s.review_score,
    s.total_price,
    s.penalty_cost
FROM supply_chain s
JOIN state_avg sa
    ON s.customer_state = sa.customer_state
WHERE s.delay_days > sa.state_avg_delay
  AND s.review_score <= 2
ORDER BY s.delay_days DESC
LIMIT 20;
