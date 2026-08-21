/*
-------------------------------------------------------------------------------
ENUNCIADO DEL PROBLEMA: Declarantes Consecutivos de TurboTax
-------------------------------------------------------------------------------
Intuit, una empresa conocida por sus productos de declaración de impuestos como 
TurboTax y QuickBooks, ofrece múltiples versiones de estos productos.

Escribe una consulta SQL que identifique los IDs de usuario (user_id) de aquellos 
individuos que hayan presentado sus impuestos utilizando cualquier versión de 
TurboTax durante tres o más años consecutivos. Cada usuario solo puede presentar 
sus impuestos una vez al año utilizando un producto específico.

Muestra el resultado ordenado de forma ascendente por user_id.

ESQUEMA DE LA TABLA:
Tabla: filed_taxes
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| filing_id   | integer  |
| user_id     | varchar  |
| filing_date | datetime |
| product     | varchar  |
+-------------+----------+

EJEMPLO DE ENTRADA:
filed_taxes
+-----------+---------+-------------+-----------------------+
| filing_id | user_id | filing_date | product               |
+-----------+---------+-------------+-----------------------+
| 1         | 1       | 4/14/2019   | TurboTax Desktop 2019 |
| 2         | 1       | 4/15/2020   | TurboTax Deluxe       |
| 3         | 1       | 4/15/2021   | TurboTax Online       |
| 4         | 2       | 4/07/2020   | TurboTax Online       |
| 5         | 2       | 4/10/2021   | TurboTax Online       |
| 6         | 3       | 4/07/2020   | TurboTax Online       |
| 7         | 3       | 4/15/2021   | TurboTax Online       |
| 8         | 3       | 3/11/2022   | QuickBooks Desktop Pro|
| 9         | 4       | 4/15/2022   | QuickBooks Online     |
+-----------+---------+-------------+-----------------------+

EJEMPLO DE SALIDA:
+---------+
| user_id |
+---------+
| 1       |
+---------+
-------------------------------------------------------------------------------
*/


WITH user_filings AS (
  SELECT 
    user_id,
    EXTRACT(YEAR FROM filing_date) AS current_year,
    LAG(EXTRACT(YEAR FROM filing_date), 1) OVER (PARTITION BY user_id ORDER BY filing_date) AS prev_year,
    LAG(EXTRACT(YEAR FROM filing_date), 2) OVER (PARTITION BY user_id ORDER BY filing_date) AS prev_prev_year
  FROM filed_taxes
  WHERE product ILIKE '%TurboTax%'
)
SELECT DISTINCT user_id
FROM user_filings
WHERE current_year = prev_year + 1 
  AND current_year = prev_prev_year + 2
ORDER BY user_id;