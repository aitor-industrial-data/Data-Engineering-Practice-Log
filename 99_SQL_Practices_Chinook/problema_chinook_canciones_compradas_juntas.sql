/* ============================================================
   PROBLEMA - Base de datos Chinook
   ============================================================

   ENUNCIADO:

   Queremos hacer un pequeño análisis de "cesta de la compra" (market
   basket analysis) sobre las facturas de Chinook.

   Para cada canción que haya sido comprada junto a alguna otra canción
   en la misma factura al menos 2 veces distintas, encuentra su
   "canción compañera" más frecuente: aquella con la que más veces ha
   coincidido en una misma factura.

   El resultado debe mostrar:
     - Canción original y su artista
     - Canción compañera y su artista
     - Número de veces que ambas fueron compradas juntas

   Si una canción tiene varias "compañeras" empatadas en frecuencia,
   quédate con cualquiera de ellas (una sola fila por canción original).
   Ordena el resultado final por número de coincidencias descendente y,
   en caso de empate, por nombre de la canción original.

   ------------------------------------------------------------
   Dificultad: self-join de InvoiceLine contra sí misma para generar
   pares de canciones dentro de la misma factura, generación de pares
   en ambos sentidos (para poder consultar por cualquiera de las dos
   canciones), y ROW_NUMBER() para quedarnos con la pareja más
   frecuente de cada canción.
   ------------------------------------------------------------ */


-- ============================================================
-- RESOLUCIÓN
-- ============================================================

WITH pares_base AS (
    -- Pares de canciones distintas dentro de la misma factura.
    -- La condición il1.TrackId < il2.TrackId evita comparar una
    -- canción consigo misma y evita contar (A,B) y (B,A) por separado
    -- en este primer paso.
    SELECT
        il1.TrackId AS TrackA,
        il2.TrackId AS TrackB,
        il1.InvoiceId
    FROM InvoiceLine il1
    JOIN InvoiceLine il2
        ON il1.InvoiceId = il2.InvoiceId
       AND il1.TrackId < il2.TrackId
),

conteo_pares AS (
    -- Cuántas facturas distintas contienen cada pareja
    SELECT
        TrackA,
        TrackB,
        COUNT(DISTINCT InvoiceId) AS VecesJuntas
    FROM pares_base
    GROUP BY TrackA, TrackB
),

pares_bidireccionales AS (
    -- Duplicamos cada pareja en ambos sentidos, para poder buscar
    -- la "mejor compañera" de cualquiera de las dos canciones
    SELECT TrackA AS TrackOrigen, TrackB AS TrackCompanera, VecesJuntas FROM conteo_pares
    UNION ALL
    SELECT TrackB AS TrackOrigen, TrackA AS TrackCompanera, VecesJuntas FROM conteo_pares
),

mejor_compania AS (
    -- Para cada canción origen, ordenamos sus compañeras por frecuencia
    -- y nos quedamos con la número 1
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY TrackOrigen
            ORDER BY VecesJuntas DESC, TrackCompanera ASC
        ) AS posicion
    FROM pares_bidireccionales
    WHERE VecesJuntas >= 2
)

SELECT
    t1.Name    AS CancionOriginal,
    ar1.Name   AS ArtistaOriginal,
    t2.Name    AS CancionCompanera,
    ar2.Name   AS ArtistaCompanera,
    mc.VecesJuntas
FROM mejor_compania mc
JOIN Track t1        ON t1.TrackId = mc.TrackOrigen
JOIN Album al1        ON al1.AlbumId = t1.AlbumId
JOIN Artist ar1        ON ar1.ArtistId = al1.ArtistId
JOIN Track t2        ON t2.TrackId = mc.TrackCompanera
JOIN Album al2        ON al2.AlbumId = t2.AlbumId
JOIN Artist ar2        ON ar2.ArtistId = al2.ArtistId
WHERE mc.posicion = 1
ORDER BY mc.VecesJuntas DESC, CancionOriginal ASC;
