/* ============================================================
   PROBLEMA - Detección de Compras de "Álbum Completo"
   ============================================================

Contexto:
El equipo de Producto de Chinook sospecha que la mayoría de los 
usuarios compran canciones sueltas de forma impulsiva, pero quieren 
identificar a los "auténticos melómanos": aquellos clientes que 
compran álbumes casi completos en una sola transacción (factura).

Para este estudio, definiremos que una factura contiene la compra 
de un "Álbum Completo" si incluye al menos el 80% de las canciones 
totales que componen ese álbum.

Enunciado
Escribe una consulta SQL que encuentre todas las ocasiones en las 
que un cliente haya comprado el 80% o más de las canciones de
 un mismo álbum en una única factura (Invoice).
   ------------------------------------------------------------ */


-- ============================================================
-- RESOLUCIÓN
-- ============================================================

WITH album_tracks AS (
    -- 1. Total de canciones por álbum
    SELECT 
        a.AlbumId,
        a.Title,
        a.ArtistId,
        COUNT(t.TrackId) AS num_tracks
    FROM Album a
    INNER JOIN Track t ON a.AlbumId = t.AlbumId
    GROUP BY a.AlbumId, a.Title, a.ArtistId
),

invoice_tracks AS (
    -- 2. Canciones de cada álbum vendidas en una misma factura
    SELECT 
        i.InvoiceId, 
        t.AlbumId, 
        i.CustomerId, 
        COUNT(il.TrackId) AS tracks_sell
    FROM InvoiceLine il
    INNER JOIN Invoice i ON il.InvoiceId = i.InvoiceId
    INNER JOIN Track t ON t.TrackId = il.TrackId
    GROUP BY i.InvoiceId, t.AlbumId, i.CustomerId
),

full_album_sell AS (
    -- 3. Filtrado por umbral del 80% con porcentaje en punto flotante
    SELECT 
        it.InvoiceId,
        it.CustomerId,
        it.AlbumId,
        at.Title,
        at.ArtistId,
        it.tracks_sell,
        at.num_tracks,
        ROUND((it.tracks_sell * 100.0) / at.num_tracks, 2) AS percentage
    FROM invoice_tracks it
    INNER JOIN album_tracks at ON it.AlbumId = at.AlbumId
    WHERE (it.tracks_sell * 100.0) / at.num_tracks >= 80
)

SELECT 
    i.InvoiceId,
    i.InvoiceDate,
    c.FirstName || ' ' || c.LastName AS Full_name,
    f.Title AS Album_title,
    ar.Name AS Artist_name,
    f.tracks_sell AS CancionesCompradas,
    f.num_tracks AS TotalCancionesAlbum,
    f.percentage AS PorcentajeComprado
FROM Invoice i
INNER JOIN full_album_sell f ON f.InvoiceId = i.InvoiceId
INNER JOIN Customer c ON c.CustomerId = i.CustomerId
INNER JOIN Artist ar ON ar.ArtistId = f.ArtistId
ORDER BY PorcentajeComprado DESC, i.InvoiceDate DESC;