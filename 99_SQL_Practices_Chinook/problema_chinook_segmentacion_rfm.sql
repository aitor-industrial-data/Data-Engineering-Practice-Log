/* ============================================================
   PROBLEMA - Base de datos Chinook
   ============================================================

   ENUNCIADO:

   Realiza una segmentación RFM (Recencia, Frecuencia, Monetario) de
   los clientes de Chinook:

     - RECENCIA: días transcurridos entre la última factura de cada
       cliente y la fecha de la última factura registrada en TODA la
       base de datos (cuanto menos días, mejor).
     - FRECUENCIA: número de facturas distintas del cliente.
     - MONETARIO: gasto total del cliente (suma de UnitPrice*Quantity).

   Para cada una de las tres dimensiones, clasifica a los clientes en
   4 cuartiles (usando NTILE), donde el cuartil 4 representa siempre
   "lo mejor" (más reciente, más frecuente o mayor gasto, según la
   dimensión) y el cuartil 1 representa "lo peor".

   Con los tres cuartiles (R, F, M) construye:
     - Un score RFM combinado (por ejemplo, concatenando o combinando
       los tres dígitos, p.ej. R=4,F=3,M=4 -> 434)
     - Un segmento textual según estas reglas (en este orden de
       prioridad):
         · "Campeón"          si R=4, F=4 y M=4
         · "En riesgo"        si R=1 y F>=3 y M>=3
                              (compraba mucho y mucho, pero hace tiempo
                              que no vuelve)
         · "Nuevo prometedor" si R=4 y F<=2
         · "Otro"             en cualquier otro caso

   Muestra cliente, días sin comprar, frecuencia, gasto total, los
   tres cuartiles, el score combinado y el segmento. Ordena por score
   RFM descendente.

   ------------------------------------------------------------
   Dificultad: combina agregaciones múltiples, una fecha de referencia
   calculada dinámicamente, NTILE() para cuartiles (con cuidado en el
   sentido del ORDER BY según la dimensión) y lógica de negocio con
   CASE anidado sobre esos cuartiles.
   ------------------------------------------------------------ */


-- ============================================================
-- RESOLUCIÓN
-- ============================================================

WITH metricas_cliente AS (
    -- Recencia (fecha de última compra), frecuencia y gasto por cliente
    SELECT
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS Cliente,
        MAX(i.InvoiceDate)                       AS UltimaCompra,
        COUNT(DISTINCT i.InvoiceId)               AS Frecuencia,
        SUM(il.UnitPrice * il.Quantity)           AS Monetario
    FROM Customer c
    JOIN Invoice i      ON i.CustomerId = c.CustomerId
    JOIN InvoiceLine il ON il.InvoiceId = i.InvoiceId
    GROUP BY c.CustomerId, Cliente
),

fecha_referencia AS (
    -- Fecha de la última factura en toda la base de datos
    SELECT MAX(InvoiceDate) AS FechaMax
    FROM Invoice
),

recencia AS (
    SELECT
        m.*,
        CAST(julianday(fr.FechaMax) - julianday(m.UltimaCompra) AS INTEGER) AS DiasSinComprar
    FROM metricas_cliente m
    CROSS JOIN fecha_referencia fr
),

cuartiles AS (
    -- NTILE(4) reparte a los clientes en 4 grupos según el ORDER BY.
    -- En Recencia ordenamos DESCENDENTE (más días primero) para que
    -- el cuartil 4 quede para quienes tienen MENOS días sin comprar
    -- (es decir, los más recientes = mejores).
    -- En Frecuencia y Monetario ordenamos ASCENDENTE para que el
    -- cuartil 4 sea para los valores más altos.
    SELECT
        *,
        NTILE(4) OVER (ORDER BY DiasSinComprar DESC) AS R,
        NTILE(4) OVER (ORDER BY Frecuencia ASC)       AS F,
        NTILE(4) OVER (ORDER BY Monetario ASC)        AS M
    FROM recencia
)

SELECT
    Cliente,
    DiasSinComprar,
    Frecuencia,
    ROUND(Monetario, 2) AS GastoTotal,
    R, F, M,
    (R * 100 + F * 10 + M) AS ScoreRFM,
    CASE
        WHEN R = 4 AND F = 4 AND M = 4        THEN 'Campeón'
        WHEN R = 1 AND F >= 3 AND M >= 3       THEN 'En riesgo'
        WHEN R = 4 AND F <= 2                  THEN 'Nuevo prometedor'
        ELSE 'Otro'
    END AS Segmento
FROM cuartiles
ORDER BY ScoreRFM DESC;
