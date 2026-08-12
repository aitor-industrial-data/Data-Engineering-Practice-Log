/*
================================================================================
EJERCICIO SQL: BASE DE DATOS CHINOOK
Reto: Segmentación de Clientes mediante Matriz RFM (Recency, Frequency, Monetary)
================================================================================

CONTEXTO:
El equipo de Business Intelligence de Chinook quiere implementar un modelo de 
Segmentación RFM para clasificar la base de clientes según su comportamiento 
de compra. Este análisis evalúa tres dimensiones clave:

  * Recencia (R): Cuántos días han pasado desde su última compra.
  * Frecuencia (F): Cuántas transacciones (facturas) ha realizado en total.
  * Monto (M): Cuánto dinero se ha gastado en total.

--------------------------------------------------------------------------------
ENUNCIADO:
Escribe una consulta SQL que calcule las métricas RFM de cada cliente y le 
asigne un Segmento de Valor automático basándose en reglas de negocio.

REQUISITOS DE LA CONSULTA:

1. Punto de Referencia Temporal (Recencia):
   - Toma la fecha de la factura más reciente de toda la base de datos como 
     "Fecha Actual" del sistema: (SELECT MAX(InvoiceDate) FROM Invoice).
   - Para cada cliente, calcula los días transcurridos entre esa "Fecha Actual" 
     y la fecha de su última compra registrada. 
     En SQLite puedes restar días con:
     JULIANDAY(FechaMax) - JULIANDAY(FechaUltimaCompra)

2. Métricas de Frecuencia y Monto:
   - Frecuencia: Número total de facturas asociadas al cliente (COUNT(InvoiceId)).
   - Monto: Suma total facturada al cliente (SUM(Total)), redondeada a 2 decimales.

3. Reglas de Segmentación (CASE WHEN):
   - 'Campeón': Clientes con recencia <= 180 días Y un gasto total > $45.00.
   - 'En Riesgo': Clientes que llevan más de 365 días sin comprar (> 365 días) 
     pero que en el pasado hicieron 3 o más compras (>= 3 facturas).
   - 'Promedio / Estándar': Todos los demás clientes que no cumplan los 
     criterios anteriores.

4. Columnas de salida:
   - ClienteId: ID del cliente (Customer.CustomerId).
   - NombreCliente: Nombre completo concatenado (FirstName + ' ' + LastName).
   - DiasUltimaCompra: Días transcurridos desde la última compra (CAST(... AS INTEGER)).
   - NumeroFacturas: Total de facturas del cliente.
   - GastoTotal: Suma total gastada.
   - Segmento: La categoría asignada ('Campeón', 'En Riesgo' o 'Promedio / Estándar').

5. Ordenación:
   - Ordena el resultado de menor a mayor por DiasUltimaCompra (los clientes 
     más recientes primero) y, en caso de empate, de mayor a menor por GastoTotal.

--------------------------------------------------------------------------------
PISTAS CONCEPTUALES:
1. Te resultará cómodo usar una primera CTE para obtener la fecha máxima global.
2. Crea una segunda CTE para agrupar por cliente, obteniendo su MAX(InvoiceDate), 
   COUNT(InvoiceId) y SUM(Total).
3. En la consulta final (o CTE de métricas), calcula la diferencia en días y 
   aplica la estructura condicional CASE WHEN para categorizar a cada usuario.
================================================================================
*/

WITH DiasUltimaCompra AS (
    SELECT 
        c.CustomerId AS ClienteId,
        c.FirstName || ' ' || c.LastName AS NombreCliente,
        MAX(i.InvoiceDate) AS UltimaFactura,
        CAST(
            (SELECT JULIANDAY(MAX(InvoiceDate)) FROM Invoice) - JULIANDAY(MAX(i.InvoiceDate)) 
            AS INTEGER
        ) AS DiasUltimaCompra,
        COUNT(i.InvoiceId) AS NumeroFacturas,
        ROUND(COALESCE(SUM(i.Total), 0), 2) AS GastoTotal
    FROM Customer c
    LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName
)

SELECT 
    ClienteId,
    NombreCliente,
    DiasUltimaCompra,
    NumeroFacturas,
    GastoTotal,
    CASE
        WHEN DiasUltimaCompra <= 180 AND GastoTotal > 45 THEN 'Campeón'
        WHEN DiasUltimaCompra > 365 AND NumeroFacturas >= 3 THEN 'En Riesgo'
        ELSE 'Estándar'
    END AS Segmento
FROM DiasUltimaCompra
ORDER BY DiasUltimaCompra ASC, GastoTotal DESC;