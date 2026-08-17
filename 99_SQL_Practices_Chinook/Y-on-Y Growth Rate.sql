/*
===============================================================================
Problem: Y-on-Y Growth Rate (Wayfair SQL Interview Question)
Source: DataLemur / Ace the Data Science Interview (#32)
===============================================================================

Assume you're given a table containing information about Wayfair user transactions 
for different products. Write a query to calculate the year-on-year growth rate 
for the total spend of each product, grouping the results by product ID.

The output should include the year in ascending order, product ID, current year's 
spend, previous year's spend and year-on-year growth percentage, rounded to 2 
decimal places.

user_transactions Table:
+------------------+----------+
| Column Name      | Type     |
+------------------+----------+
| transaction_id   | integer  |
| product_id       | integer  |
| spend            | decimal  |
| transaction_date | datetime |
+------------------+----------+

user_transactions Example Input:
+----------------+------------+---------+---------------------+
| transaction_id | product_id | spend   | transaction_date    |
+----------------+------------+---------+---------------------+
| 1341           | 123424     | 1500.60 | 12/31/2019 12:00:00 |
| 1423           | 123424     | 1000.20 | 12/31/2020 12:00:00 |
| 1623           | 123424     | 1246.44 | 12/31/2021 12:00:00 |
| 1322           | 123424     | 2145.32 | 12/31/2022 12:00:00 |
+----------------+------------+---------+---------------------+

Example Output:
+------+------------+-----------------+-----------------+----------+
| year | product_id | curr_year_spend | prev_year_spend | yoy_rate |
+------+------------+-----------------+-----------------+----------+
| 2019 | 123424     | 1500.60         | NULL            | NULL     |
| 2020 | 123424     | 1000.20         | 1500.60         | -33.35   |
| 2021 | 123424     | 1246.44         | 1000.20         | 24.62    |
| 2022 | 123424     | 2145.32         | 1246.44         | 72.12    |
+------+------------+-----------------+-----------------+----------+
===============================================================================
*/

WITH current_year_sales AS (
  SELECT 
    product_id,
    ROUND(SUM(spend), 2) AS total_spend,
    EXTRACT(YEAR FROM transaction_date) AS transaction_year
  FROM user_transactions
  GROUP BY product_id, EXTRACT(YEAR FROM transaction_date)
),

previous_year_sales AS (
  SELECT 
    product_id,
    ROUND(SUM(spend), 2) AS total_spend,
    EXTRACT(YEAR FROM transaction_date) AS transaction_year
  FROM user_transactions
  GROUP BY product_id, EXTRACT(YEAR FROM transaction_date)
)

SELECT 
  curr.transaction_year AS year,
  curr.product_id,
  curr.total_spend AS curr_year_spend,
  prev.total_spend AS prev_year_spend,
  ROUND((curr.total_spend - COALESCE(prev.total_spend, 0.0)) * 100.0 / prev.total_spend, 2) AS yoy_rate
FROM current_year_sales curr
LEFT JOIN previous_year_sales prev 
  ON curr.product_id = prev.product_id 
 AND curr.transaction_year - 1 = prev.transaction_year
ORDER BY curr.product_id ASC, curr.transaction_year ASC;