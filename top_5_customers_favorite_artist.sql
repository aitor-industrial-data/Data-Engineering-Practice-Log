/* ============================================================
   PROBLEMA - Base de datos Chinook
   ============================================================

   ENUNCIADO:

   Escribe una consulta SQL que devuelva los 5 clientes con mayor
   gasto acumulado en la tienda y, junto a cada uno, el artista del 
   cual han adquirido el mayor número de canciones.*/

-- ============================================================
-- RESOLUCIÓN
-- ============================================================

WITH Vip_Customers AS (
    -- 1. Obtenemos los 5 mejores clientes por gasto acumulado
    SELECT 
        c.CustomerId, 
        c.FirstName, 
        c.LastName, 
        SUM(i.Total) AS Total_gastado
    FROM Customer c
    INNER JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName
    ORDER BY Total_gastado DESC
    LIMIT 5
),
vip_tracks AS (
    -- 2. Obtenemos el detalle de canciones compradas por estos 5 clientes
    SELECT 
        v.CustomerId, 
        il.TrackId, 
        il.Quantity
    FROM Invoice i
    INNER JOIN Vip_Customers v ON v.CustomerId = i.CustomerId
    INNER JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
),
vip_composers AS (
    -- 3. Agrupamos y sumamos la cantidad de canciones por cliente y artista
    SELECT 
        vt.CustomerId, 
        a.Name AS Artist_Name, 
        SUM(vt.Quantity) AS Quantity
    FROM vip_tracks vt
    INNER JOIN Track t ON vt.TrackId = t.TrackId
    INNER JOIN Album al ON t.AlbumId = al.AlbumId
    INNER JOIN Artist a ON al.ArtistId = a.ArtistId
    GROUP BY vt.CustomerId, a.Name
),
vip_ranking AS (
    -- 4. Rankeamos los artistas por cliente ordenados por volumen comprado
    SELECT 
        vc.CustomerId,
        vc.Artist_Name,
        vc.Quantity,
        ROW_NUMBER() OVER(PARTITION BY vc.CustomerId ORDER BY vc.Quantity DESC) AS ranking
    FROM vip_composers vc
)
-- 5. Seleccionamos únicamente el artista #1 por cliente
SELECT 
    r.CustomerId, 
    c.FirstName || ' ' || c.LastName AS Full_Name, 
    r.Artist_Name, 
    r.Quantity
FROM vip_ranking r
JOIN Vip_Customers c ON r.CustomerId = c.CustomerId
WHERE r.ranking = 1
ORDER BY c.Total_gastado DESC;