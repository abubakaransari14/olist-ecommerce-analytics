SELECT 
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS MonthYear,
    ROUND(SUM(oi.item_total_value), 2) AS totalRevenue
FROM 
    olist_db.orders o
LEFT JOIN 
    olist_db.order_items oi ON o.order_id = oi.order_id
WHERE 
    o.order_status = 'delivered'
GROUP BY 
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY 
    MonthYear ASC;
    
-- Monthly Order
SELECT
    DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m') AS MONTHYEAR,
    COUNT(DISTINCT(o.order_id)) AS ORDERS
FROM
    olist_db.orders o
GROUP BY DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m');

-- REVENUE BY STATE
SELECT 
	c.customer_state,
	round(sum(oi.item_total_value),2) REVENUE
FROM olist_db.order_items oi
LEFT JOIN olist_db.orders o ON oi.order_id = o.order_id
LEFT JOIN olist_db.customers c ON o.customer_id = c.customer_id  
GROUP BY c.customer_state
ORDER BY REVENUE DESC;

-- SELECT TOP 10 CITIES
SELECT
	c.customer_city,
    c.customer_state,
	ROUND(SUM(oi.item_total_value),2) REVENUE
FROM olist_db.order_items oi
LEFT JOIN olist_db.orders o ON oi.order_id = o.order_id
LEFT JOIN olist_db.customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_city, c.customer_state
ORDER BY REVENUE DESC 
LIMIT 10;

-- TOP PRODUCT CATEGORY
SELECT
	p.product_category_name,
    ROUND(SUM(oi.item_total_value),2) AS REVENUE
FROM olist_db.order_items oi
LEFT JOIN olist_db.products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY REVENUE DESC
LIMIT 10;

-- AVERAGE REVENUE (APPROACH 01) 160.58
SELECT 
	ROUND(AVG (LISTREVENUE.REVENUE),2) AS AVERAGE_REVENUE
FROM (SELECT
	oi.order_id,
	SUM(oi.item_total_value) AS REVENUE
FROM olist_db.order_items oi
GROUP BY oi.order_id) LISTREVENUE;

-- AVERAGE REVENUE (APPROACH 02) 160.58
WITH ORDER_REVENUE AS (SELECT
	oi.order_id,
	SUM(oi.item_total_value) AS REVENUE
FROM olist_db.order_items oi
GROUP BY oi.order_id)
SELECT 
	ROUND(AVG(ORDER_REVENUE.REVENUE),2) AS AVERAGE_REVENUE
FROM  ORDER_REVENUE;

-- ORDER STATUS
SELECT
	o.order_status,
	COUNT(DISTINCT(o.order_id)) AS ORDER_COUNT,
    ROUND(
		(COUNT(DISTINCT(o.order_id)) *100  /  SUM(COUNT(DISTINCT(o.order_id))) over()) ,2
    ) as sharePercentage
FROM olist_db.orders o
GROUP BY o.order_status
ORDER BY sharePercentage DESC;

-- Payment Analysis
SELECT
	p.payment_type,
    COUNT(DISTINCT p.order_id) AS Orders,
    SUM(p.payment_value) AS TotalPaymentValue,
    AVG(p.payment_value) AS AveragePaymentValue
FROM olist_db.order_payments p
GROUP BY p.payment_type;

-- Delivery Performance
SELECT
	ROUND(AVG(o.delivery_days),2) AS AVG_DELIVERY_DAYS,
    ROUND(AVG(o.delivery_delay_days),2) AS AVG_DELIVERY_DELAY,
    SUM(
		CASE 
			WHEN is_late = 1
            THEN 1
            ELSE 0
		END
    ) AS LATE_ORDER,
    COUNT(*) AS TOTAL_ORDER
FROM olist_db.orders o;

-- Delivery Performance approach 2
SELECT
	ROUND(AVG(o.delivery_days),2) AS AVG_DELIVERY_DAYS,
    ROUND(AVG(o.delivery_delay_days),2) AS AVG_DELIVERY_DELAY,
    SUM(is_late) AS LATE_ORDER,
    COUNT(*) AS TOTAL_ORDER
FROM olist_db.orders o;

-- Late Delivery Rate by State
SELECT 
    c.customer_state,
	COUNT(*) AS TOTAL_ORDER,
    SUM(
		CASE 
			WHEN is_late = 1
            THEN 1
            ELSE 0
		END
    ) as LATE_BY_STATE,
    ROUND(
			SUM(
				CASE 
					WHEN is_late = 1
					THEN 1
					ELSE 0
				END
			) * 100 / COUNT(*)
    ,2) AS LATE_PERCENT
FROM olist_db.orders o
LEFT JOIN olist_db.customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
HAVING COUNT(*) >= 100
ORDER BY LATE_PERCENT DESC;

-- Review Score
SELECT
    r.review_score,
    COUNT(*) AS ReviewCount,
    CAST(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER()
        AS DECIMAL(10,2)
    ) AS Percentage
FROM olist_db.order_reviews r
GROUP BY r.review_score;

-- Late Delivery vs Review Score 
SELECT
	CASE
		WHEN o.delivery_delay_days IS NULL THEN 'CANCELLED'
		WHEN o.delivery_delay_days <= 0 THEN 'ON TIME'
        ELSE 'DELAY'
	END AS statusE,
    COUNT(DISTINCT(o.order_id)) as totalOrder,
    ROUND(AVG(r.review_score),2) as avgReview
FROM olist_db.orders o
LEFT JOIN olist_db.order_reviews r ON o.order_id = r.order_id
GROUP BY statusE;

-- REPEAT CUSTOMERS
SELECT
	c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS NUMBER_OF_ORDERS
FROM olist_db.orders o
LEFT JOIN olist_db.customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_unique_id
HAVING NUMBER_OF_ORDERS > 1
ORDER BY NUMBER_OF_ORDERS DESC;
-- Customer Revenue
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS Orders,
    SUM(oi.item_total_value) AS Revenue
FROM olist_db.orders o
LEFT JOIN olist_db.customers c ON o.customer_id = c.customer_id
LEFT JOIN olist_db.order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY Revenue DESC
LIMIT 20;

-- MONTHLY REVENUE
SELECT
    DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m') as YEARMONTH,
    p.product_category_name,
    ROUND(SUM(oi.item_total_value)) AS Revenue
FROM olist_db.order_items oi
LEFT JOIN olist_db.orders o ON oi.order_id = o.order_id
LEFT JOIN olist_db.products p ON oi.product_id = p.product_id
GROUP BY YEARMONTH, p.product_category_name
ORDER BY YEARMONTH, Revenue DESC;

-- Revenue Ranking by State
SELECT
    customer_state,
    Revenue,
    RANK() OVER (
        ORDER BY Revenue DESC
    ) AS RevenueRank
FROM
(
    SELECT
        c.customer_state,
        SUM(oi.item_total_value) AS Revenue
FROM olist_db.order_items oi
LEFT JOIN olist_db.orders o ON oi.order_id = o.order_id
LEFT JOIN olist_db.customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
) AS StateRevenue
ORDER BY RevenueRank;

-- Running Monthly Revenue
WITH MONTHLYREVEUNE AS(
	SELECT 
		DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m') AS MONTHYEAR,
		ROUND(SUM((oi.item_total_value)), 2) AS Revenue
	FROM olist_db.orders o
	LEFT JOIN olist_db.order_items oi ON o.order_id = oi.order_id
	GROUP BY MONTHYEAR
)
SELECT
	MONTHYEAR,
    Revenue,
    ROUND(SUM(Revenue) OVER (ORDER BY MONTHYEAR),2) AS CumulativeRevenue
FROM MONTHLYREVEUNE
ORDER BY MONTHYEAR;

-- month over month
WITH MONTHLYREVEUNE AS(
	SELECT 
		DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m') AS MONTHYEAR,
		ROUND(SUM((oi.item_total_value)), 2) AS Revenue
	FROM olist_db.orders o
	LEFT JOIN olist_db.order_items oi ON o.order_id = oi.order_id
	GROUP BY MONTHYEAR
),
REVENUEWITHPREVIOUS AS
(
	SELECT 
		MONTHYEAR,
        Revenue,
        LAG (Revenue) OVER (ORDER BY MONTHYEAR) AS PREVIOUSMONTHREV
	FROM MONTHLYREVEUNE 
)
SELECT 
	MONTHYEAR,
    Revenue,
    PREVIOUSMONTHREV,
    CAST(
		(Revenue - PREVIOUSMONTHREV)/
        NULLIF(PREVIOUSMONTHREV,0) * 100
        AS DECIMAL(10,2)
    ) AS MONTHLYPERCENTAGE
FROM REVENUEWITHPREVIOUS
ORDER BY MONTHYEAR