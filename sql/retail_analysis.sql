create database retail_analysis;
use retail_analysis;



SELECT
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    SUM(Quantity) AS total_units_sold,
    COUNT(DISTINCT CustomerID) AS unique_customers,
    COUNT(DISTINCT StockCode) AS unique_products,
    ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2)
        AS average_order_value
FROM retail_sales;


USE retail_analysis;
SHOW TABLES;


SELECT COUNT(*) AS total_records


SELECT
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    SUM(Quantity) AS total_units_sold,
    COUNT(DISTINCT CustomerID) AS unique_customers,
    COUNT(DISTINCT StockCode) AS unique_products,
    ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2)
        AS average_order_value
FROM retail_analysis;
