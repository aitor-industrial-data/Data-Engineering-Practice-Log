-- ============================================================================
-- Nombre del archivo: chinook_customer_genre_distribution.sql
-- Base de Datos: Chinook (SQLite / PostgreSQL)
-- Nivel: Intermedio-Avanzado (CTEs & Window Functions)
-- ============================================================================
--
-- EL PROBLEMA: Análisis de Distribución de Géneros por Cliente
--
-- Encuentra a los clientes que han comprado canciones de al menos 3 géneros 
-- musicales distintos, mostrando cuál es su género preferido (el género del que 
-- más canciones han comprado) y el total que han gastado en la plataforma.
--
-- REQUISITOS DE LA CONSULTA:
-- 1. Devuelve las siguientes columnas:
--    - CustomerName: Nombre y apellidos concatenados (FirstName + ' ' + LastName).
--    - TotalGenres: Número total de géneros distintos que ha comprado ese cliente.
--    - TopGenre: El nombre del género del cual ha comprado más canciones.
--    - TotalSpent: Suma total gastada por el cliente en todas sus compras 
--      (calculada desde las líneas de factura para evitar duplicados), 
--      redondeada a 2 decimales.
--
-- 2. Filtra para mostrar únicamente a los clientes cuyo TotalGenres sea mayor 
--    o igual a 3.
--
-- 3. Ordena los resultados por TotalSpent de mayor a menor.
--
-- TABLAS INVOLUCRADAS: Customer, Invoice, InvoiceLine, Track, Genre
--
-- PISTAS / FUNCIONES RECOMENDADAS:
-- - Usa ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) para ranking de géneros.
-- - Para evitar inflación de datos (fan-out) usa SUM(il.Quantity * il.UnitPrice).
--
-- ============================================================================

with genre_quantity_sales as (
	SELECT c.customerId,g.GenreId,
		g.name,
		sum(il.quantity),
		row_number() over(partition by c.CustomerId	order by sum(il.quantity) desc) as genrerank
	from Customer c
	inner join invoice i on i.CustomerId=c.CustomerId
	inner join InvoiceLine il on il.InvoiceId=i.InvoiceId
	inner JOIN Track t on t.TrackId= il.trackid
	inner join genre g on g.GenreId=t.GenreId
	group by c.CustomerId, g.GenreId
),
Sales_customer as(
	SELECT c.customerId,
		c.FirstName||' '||c.LastName as FullName,
	count(distinct(g.genreId)) as TotalGenres,
	round(sum(il.Quantity*il.UnitPrice),2) as TotalSpent
from Customer c
inner join invoice i on i.CustomerId=c.CustomerId
inner join InvoiceLine il on il.InvoiceId=i.InvoiceId
inner JOIN Track t on t.TrackId= il.trackid
inner join genre g on g.GenreId=t.GenreId
group by c.CustomerId
having TotalGenres >=3
)

SELECT s.customerId,s.FullName as CustomerName,
	s.TotalGenres,
	g.name as TopGenre,
	s.TotalSpent
from genre_quantity_sales g
INNER join Sales_customer s on s.CustomerId=g.CustomerId
where genrerank=1
order by TotalSpent desc
;