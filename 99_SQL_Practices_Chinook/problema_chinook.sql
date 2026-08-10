WITH country_sells AS (
    SELECT 
        c.Country AS Pais,
        g.Name AS Genero,
        SUM(il.UnitPrice * il.Quantity) AS TotalFacturado,
        SUM(il.Quantity) AS TotalCanciones
    FROM Track t
    INNER JOIN InvoiceLine il ON t.TrackId = il.TrackId
    INNER JOIN Genre g ON t.GenreId = g.GenreId
    INNER JOIN Invoice i ON i.InvoiceId = il.InvoiceId
    INNER JOIN Customer c ON i.CustomerId = c.CustomerId
    GROUP BY c.Country, g.GenreId, g.Name
),
rankin AS (
    SELECT 
        Pais,
        Genero,
        TotalFacturado,
        TotalCanciones,
        ROW_NUMBER() OVER (
            PARTITION BY Pais 
            ORDER BY TotalFacturado DESC, TotalCanciones DESC
        ) AS ranking
    FROM country_sells
)
SELECT 
    Pais,
    Genero,
    ROUND(TotalFacturado, 2) AS TotalFacturado
FROM rankin
WHERE ranking = 1
ORDER BY Pais ASC;