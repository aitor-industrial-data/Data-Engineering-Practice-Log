-- PASO 1: Capturamos la fecha de la factura anterior usando el primer LAG
WITH historial_compras AS (
    SELECT 
        c.CustomerId AS cliente_id,
        c.FirstName || ' ' || c.LastName AS nombre_completo,
        i.InvoiceId,
        i.InvoiceDate AS fecha_factura_actual,
        
        -- Obtiene la fecha de la compra previa del mismo cliente
        LAG(i.InvoiceDate) OVER (
            PARTITION BY c.CustomerId 
            ORDER BY i.InvoiceDate ASC, i.InvoiceId ASC
        ) AS fecha_factura_anterior
    FROM Customer c
    INNER JOIN Invoice i ON c.CustomerId = i.CustomerId
),

-- PASO 2: Calculamos la diferencia en días y aplicamos un segundo LAG para el intervalo previo
intervalos_compras AS (
    SELECT 
        cliente_id,
        nombre_completo,
        fecha_factura_actual,
        fecha_factura_anterior,
        
        -- Cálculo de días entre la compra actual y la anterior (SQLite usa JULIANDAY)
        CAST(ROUND(JULIANDAY(fecha_factura_actual) - JULIANDAY(fecha_factura_anterior)) AS INTEGER) AS dias_intervalo_actual,
        
        -- Encadenamos un segundo LAG sobre la diferencia de días recién calculada
        LAG(
            CAST(ROUND(JULIANDAY(fecha_factura_actual) - JULIANDAY(fecha_factura_anterior)) AS INTEGER)
        ) OVER (
            PARTITION BY cliente_id 
            ORDER BY fecha_factura_actual ASC
        ) AS dias_intervalo_previo
    FROM historial_compras
    WHERE fecha_factura_anterior IS NOT NULL -- Descarta la 1ª compra del cliente (no tiene previa)
)

-- PASO 3: Filtramos clientes que cumplen el criterio de desaceleración (>= 2x)
SELECT 
    cliente_id,
    nombre_completo,
    DATE(fecha_factura_actual) AS fecha_factura_actual,
    DATE(fecha_factura_anterior) AS fecha_factura_anterior,
    dias_intervalo_actual,
    dias_intervalo_previo,
    
    -- Métrica visual de desaceleración
    ROUND(CAST(dias_intervalo_actual AS REAL) / dias_intervalo_previo, 2) || 'x' AS factor_desaceleracion
FROM intervalos_compras
WHERE dias_intervalo_previo IS NOT NULL 
  AND dias_intervalo_previo > 0
  AND dias_intervalo_actual >= (2 * dias_intervalo_previo)
ORDER BY (dias_intervalo_actual / dias_intervalo_previo) DESC;