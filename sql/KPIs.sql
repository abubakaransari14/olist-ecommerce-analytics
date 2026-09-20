CREATE DATABASE IF NOT EXISTS olist_db;
-- Total Orders
SELECT 
    COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM 
    olist_db.orders;

-- Total Customer  
SELECT 
    COUNT(DISTINCT customer_unique_id) AS TOTAL_CUSTOMER
FROM 
    olist_db.customers;

-- Total Products
SELECT 
	COUNT(DISTINCT product_id) AS TOTAL_PRODUCTS
FROM 
    olist_db.products;
    
-- Total Products
SELECT 
	COUNT(DISTINCT product_id) AS TOTAL_PRODUCTS
FROM 
    olist_db.products;

-- TOTAL SELLERS
SELECT 
	COUNT(DISTINCT seller_id) AS  TOTAL_SELLERS
FROM 
    olist_db.sellers;

-- TOTAL CUSTOMER CITIES
SELECT 
	COUNT(DISTINCT customer_city) AS  TOTAL_CUSTOMER_CITIES
FROM 
    olist_db.customers;
    
-- TOTAL CUSTOMER STATE
SELECT 
	COUNT(DISTINCT customer_state) AS  TOTAL_CUSTOMER_STATES
FROM 
    olist_db.customers;

