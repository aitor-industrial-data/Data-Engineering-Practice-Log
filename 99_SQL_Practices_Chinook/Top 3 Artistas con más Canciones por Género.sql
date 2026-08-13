-- =============================================================================
-- ENUNCIADO: TOP 3 ARTISTAS POR GÉNERO MUSICAL
-- =============================================================================
-- Escribe una consulta SQL que liste el Top 3 de artistas para cada género
-- musical, mostrando su posición dentro del ranking del género.
--
-- Requisitos de la consulta:
--
-- 1. Métricas y Ranking:
--    - Cuenta el número total de canciones (Track.TrackId) por cada combinación
--      de Género y Artista.
--    - Asigna una posición mediante DENSE_RANK() particionando por Género
--      y ordenando de mayor a menor por el total de canciones.
--
-- 2. Filtrado:
--    - Muestra únicamente los artistas que queden dentro del Top 3
--      (PosicionRanking <= 3) de su respectivo género.
--
-- 3. Columnas de salida:
--    - Genero: Nombre del género (Genre.Name).
--    - Artista: Nombre del artista (Artist.Name).
--    - TotalCanciones: Número total de canciones de ese artista en ese género.
--    - PosicionRanking: Número de ranking (1, 2 o 3).
--
-- 4. Ordenación:
--    - Ordena por Genero alfabéticamente y por PosicionRanking en orden ascendente.
-- =============================================================================


WITH GenreRank as(
	SELECT g.Name as Genero, ar.Name as Artista, count(t.trackid) as TotalCanciones,
		DENSE_RANK() OVER(partition by g.GenreId ORDER by count(t.trackid) DESC) as PosicionRanking
	FROM track t
	INNER JOIN genre g on g.GenreId = t.GenreId
	inner JOIN album al on t.AlbumId = al.AlbumId
	INNER JOIN Artist ar on ar.ArtistId = al.ArtistId
	group by g.GenreId, ar.Name,ar.ArtistId,ar.Name
)

SELECT *
FROM GenreRank
WHERE PosicionRanking<=3
ORDER by Genero ASC,PosicionRanking ASC
;