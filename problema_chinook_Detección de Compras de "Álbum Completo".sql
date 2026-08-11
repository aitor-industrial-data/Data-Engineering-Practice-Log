/* ============================================================
   PROBLEMA - Base de datos Chinook
   ============================================================

   ENUNCIADO:

   Analiza la evolución mensual de los ingresos totales de la tienda
   (todas las facturas, sin distinguir cliente) y calcula, para cada
   mes:

     - El ingreso total de ese mes
     - La MEDIA MÓVIL de los últimos 3 meses (el mes actual + los 2
       anteriores)
     - El INGRESO ACUMULADO desde el primer mes con datos hasta ese mes
     - El PORCENTAJE DE VARIACIÓN respecto al mes inmediatamente
       anterior
     - Una columna de aviso que marque 'ALERTA' cuando la caída
       respecto al mes anterior sea superior al 15% (es decir, una
       bajada fuerte de ingresos)

   Ordena el resultado cronológicamente por mes.

   ------------------------------------------------------------
   Dificultad: análisis de series temporales con funciones de ventana
   sobre un frame explícito (ROWS BETWEEN ... AND ...) para la media
   móvil y el acumulado, más LAG() para comparar contra el mes
   anterior y lógica de negocio (umbral de alerta) sobre el resultado.
   ------------------------------------------------------------ */


-- ============================================================
-- RESOLUCIÓN
-- ============================================================

WITH ingresos_mensuales AS (
    -- Ingreso total agrupado por mes (usamos Invoice.Total, que ya
    -- viene precalculado como el total de cada factura)
    SELECT
        strftime('%Y-%m', InvoiceDate) AS Mes,
        SUM(Total) AS IngresoMes
    FROM Invoice
    GROUP BY Mes
),

con_ventanas AS (
    SELECT
        Mes,
        IngresoMes,
        -- Media de este mes y los 2 anteriores (3 meses en total)
        AVG(IngresoMes) OVER (
            ORDER BY Mes
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS MediaMovil3M,
        -- Suma acumulada desde el primer mes disponible
        SUM(IngresoMes) OVER (
            ORDER BY Mes
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS IngresoAcumulado,
        -- Ingreso del mes inmediatamente anterior, para comparar
        LAG(IngresoMes) OVER (ORDER BY Mes) AS IngresoMesAnterior
    FROM ingresos_mensuales
)

SELECT
    Mes,
    ROUND(IngresoMes, 2)         AS IngresoMes,
    ROUND(MediaMovil3M, 2)       AS MediaMovil3M,
    ROUND(IngresoAcumulado, 2)   AS IngresoAcumulado,
    CASE
        WHEN IngresoMesAnterior IS NULL THEN NULL
        ELSE ROUND(100.0 * (IngresoMes - IngresoMesAnterior) / IngresoMesAnterior, 2)
    END AS VariacionPorcentual,
    CASE
        WHEN IngresoMesAnterior IS NOT NULL
             AND (IngresoMes - IngresoMesAnterior) < -0.15 * IngresoMesAnterior
        THEN 'ALERTA'
        ELSE ''
    END AS Aviso
FROM con_ventanas
ORDER BY Mes;
