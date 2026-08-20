-- ============================================================================
-- Nombre del archivo: chinook_monthly_running_total.sql
-- Base de Datos: Chinook (SQLite / PostgreSQL)
-- Nivel: Avanzado (Window Functions & Time Series)
-- ============================================================================
--
-- EL PROBLEMA: Análisis de Ventas Acumuladas Mensuales (Running Total)
--
-- El equipo financiero quiere analizar el crecimiento histórico de ingresos de la
-- plataforma mes a mes para evaluar la tendencia del negocio.
--
-- REQUISITOS DE LA CONSULTA:
-- 1. Agrupa las facturas por año y mes (formato 'YYYY-MM').
-- 2. Devuelve las siguientes columnas:
--    - InvoiceMonth: Año y mes de la factura (ej: '2021-01').
--    - MonthlySales: Total de ingresos facturados únicamente en ese mes 
--      (redondeado a 2 decimales).
--    - RunningTotal: Suma acumulada de ingresos desde el inicio de los registros 
--      hasta el mes actual (usando funciones de ventana, redondeado a 2 decimales).
--    - MoM_Growth: Porcentaje de crecimiento del ingreso respecto al mes anterior 
--      (Month-over-Month), redondeado a 2 decimales. 
--      Fórmula: ((MonthlySales_MesActual - MonthlySales_MesAnterior) / MonthlySales_MesAnterior) * 100
--      Nota: En el primer mes del historial debe devolver NULL o 0.
--
-- 3. Ordena los resultados de forma cronológica (de más antiguo a más reciente).
--
-- TABLAS INVOLUCRADAS: Invoice
--
-- PISTA / FUNCIONES RECOMENDADAS:
-- - Funciones de fecha: strftime('%Y-%m', InvoiceDate) en SQLite o TO_CHAR() en PostgreSQL.
-- - Función de ventana para el acumulado: SUM(...) OVER (ORDER BY ...)
-- - Función de ventana para el mes anterior: LAG(...) OVER (ORDER BY ...)
--
-- ============================================================================

WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS InvoiceMonth,
        ROUND(SUM(Total), 2) AS MonthlySales
    FROM Invoice
    GROUP BY strftime('%Y-%m', InvoiceDate)
)
SELECT 
    InvoiceMonth,
    MonthlySales,
    ROUND(SUM(MonthlySales) OVER (ORDER BY InvoiceMonth), 2) AS RunningTotal,
    ROUND(
        (MonthlySales - LAG(MonthlySales) OVER (ORDER BY InvoiceMonth)) 
        * 100.0 / LAG(MonthlySales) OVER (ORDER BY InvoiceMonth), 
        2
    ) AS MoM_Growth
FROM monthly_sales
ORDER BY InvoiceMonth ASC;