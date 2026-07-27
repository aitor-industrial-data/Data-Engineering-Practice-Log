WITH invoice_gaps AS (
    -- Paso 1 y 2: Obtener la fecha anterior y calcular los días de diferencia
    SELECT 
        CustomerId,
        InvoiceId,
        InvoiceDate,
        Total,
        LAG(InvoiceDate) OVER (
            PARTITION BY CustomerId 
            ORDER BY InvoiceDate
        ) AS previous_invoice_date,
        -- Diferencia en días para SQLite (en PostgreSQL usar: JULIANDAY por DATE_PART / EXTRACT)
        ROUND(
            JULIANDAY(InvoiceDate) - JULIANDAY(
                LAG(InvoiceDate) OVER (
                    PARTITION BY CustomerId 
                    ORDER BY InvoiceDate
                )
            ), 1
        ) AS days_since_last_purchase
    FROM Invoice
)
-- Paso 3: Agrupar por cliente, agregar métricas y filtrar
SELECT 
    c.CustomerId AS customer_id,
    c.FirstName || ' ' || c.LastName AS customer_name,
    MIN(ig.InvoiceDate) AS first_purchase_date,
    MAX(ig.InvoiceDate) AS last_purchase_date,
    ROUND(SUM(ig.Total), 2) AS total_spent,
    ROUND(AVG(ig.days_since_last_purchase), 1) AS avg_days_between_purchases
FROM Customer c
JOIN invoice_gaps ig ON c.CustomerId = ig.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
HAVING COUNT(ig.InvoiceId) >= 2
ORDER BY total_spent DESC;