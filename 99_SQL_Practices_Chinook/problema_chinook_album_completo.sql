/* ============================================================
   PROBLEMA - Base de datos Chinook
   ============================================================

   ENUNCIADO:

   Determina qué facturas corresponden a la compra de un ÁLBUM
   COMPLETO. Una factura cuenta como "álbum completo" cuando el
   conjunto de canciones que contiene coincide EXACTAMENTE con el
   conjunto de canciones de un único álbum:

     - No le falta ninguna canción de ese álbum (el cliente se lo
       llevó entero).
     - No contiene canciones de ningún otro álbum ni sueltas fuera de
       ese álbum.

   Muestra: número de factura, fecha, cliente, título del álbum,
   artista y número de canciones. Solo incluye las facturas que
   cumplan la condición de álbum completo, ordenadas por fecha
   descendente.

   ------------------------------------------------------------
   Dificultad: es un problema de IGUALDAD DE CONJUNTOS (set equality)
   aplicado por factura: hay que comprobar en las dos direcciones que
   "canciones del álbum" y "canciones de la factura" son el mismo
   conjunto, usando dobles NOT EXISTS anidados, tras primero filtrar
   las facturas que solo tocan un único álbum.
   ------------------------------------------------------------ */


-- ============================================================
-- RESOLUCIÓN
-- ============================================================

WITH factura_tracks AS (
    -- Cada línea de factura con la canción y el álbum al que pertenece
    SELECT
        il.InvoiceId,
        t.TrackId,
        t.AlbumId
    FROM InvoiceLine il
    JOIN Track t ON t.TrackId = il.TrackId
),

resumen_factura AS (
    -- Por factura: a cuántos álbumes distintos pertenecen sus
    -- canciones, y cuántas canciones tiene en total
    SELECT
        InvoiceId,
        MIN(AlbumId)                 AS AlbumId,
        COUNT(DISTINCT AlbumId)      AS NumAlbumsDistintos,
        COUNT(*)                     AS NumTracksFactura
    FROM factura_tracks
    WHERE AlbumId IS NOT NULL
    GROUP BY InvoiceId
),

candidatas_un_album AS (
    -- Solo nos interesan las facturas cuyas canciones pertenecen
    -- TODAS a un único álbum (condición necesaria, no suficiente)
    SELECT *
    FROM resumen_factura
    WHERE NumAlbumsDistintos = 1
)

SELECT
    i.InvoiceId,
    i.InvoiceDate,
    c.FirstName || ' ' || c.LastName AS Cliente,
    al.Title  AS Album,
    ar.Name   AS Artista,
    cua.NumTracksFactura AS NumCanciones
FROM candidatas_un_album cua
JOIN Invoice i  ON i.InvoiceId = cua.InvoiceId
JOIN Customer c ON c.CustomerId = i.CustomerId
JOIN Album al   ON al.AlbumId = cua.AlbumId
JOIN Artist ar  ON ar.ArtistId = al.ArtistId
WHERE NOT EXISTS (
    -- ¿Existe alguna canción del álbum que NO esté en la factura?
    SELECT 1
    FROM Track t
    WHERE t.AlbumId = cua.AlbumId
      AND NOT EXISTS (
          SELECT 1
          FROM factura_tracks ft
          WHERE ft.InvoiceId = cua.InvoiceId
            AND ft.TrackId = t.TrackId
      )
)
ORDER BY i.InvoiceDate DESC;
