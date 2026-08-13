/*
===============================================================================
PROBLEMA: Informe de Ventas Anuales Pivotadas por Género
===============================================================================

ENUNCIADO:
Escribe una consulta SQL que genere un informe de ventas anuales donde los 
ingresos de los géneros principales aparezcan en columnas independientes, junto 
con el total del resto de géneros y el porcentaje que representa el género 
líder (Rock).

REQUISITOS DE LA CONSULTA:

1. Agrupación Anual:
   - Agrupa las ventas por año de la factura (STRFTIME('%Y', InvoiceDate)).

2. Columnas de salida:
   - Anio: Año en formato de 4 dígitos (YYYY).
   - VentasRock: Suma de facturación (UnitPrice * Quantity) para el género 'Rock'.
   - VentasLatin: Suma de facturación para el género 'Latin'.
   - VentasMetal: Suma de facturación para el género 'Metal'.
   - VentasOtros: Suma de facturación para todos los demás géneros restantes.
   - TotalAnio: Importe total facturado en ese año (suma de todas las líneas).
   - PctCuotaRock: Porcentaje que representan las ventas de Rock sobre el 
     total del año (VentasRock / TotalAnio) * 100, redondeado a 2 decimales.

3. Formato y Tratamiento de Nulos:
   - Todos los valores monetarios y porcentajes deben estar redondeados 
     a 2 decimales: ROUND(..., 2).
   - Si en algún año un género no tuviese ventas, debe mostrar 0.00 en lugar 
     de NULL (puedes usar COALESCE o asegurarte de retornar 0 en la rama ELSE del CASE).

4. Ordenación:
   - Ordena el resultado de forma cronológica ascendente por Anio.
===============================================================================
*/


WITH GenreSales as(
	SELECT STRFTIME('%Y', i.InvoiceDate) as anio,
		coalesce(round(SUM(CASE WHEN g.Name = 'Rock' THEN il.UnitPrice * il.Quantity ELSE 0 END),2),0.00) AS VentasRock,
		coalesce(round(SUM(CASE WHEN g.Name = 'Latin' THEN il.UnitPrice * il.Quantity ELSE 0 END),2),0.00)  AS VentasLatin,
		coalesce(round(SUM(CASE WHEN g.Name = 'Metal' THEN il.UnitPrice * il.Quantity ELSE 0 END),2),0.00)  AS VentasMetal,
		coalesce(round(SUM(CASE WHEN g.Name not in ('Rock','Latin','Metal') THEN il.UnitPrice * il.Quantity ELSE 0 END),2),0.00)  AS VentasOtros,
		coalesce(round(sum(il.UnitPrice * il.Quantity),2),0.00)  as TotalAnio
	FROM Track t
	INNER join InvoiceLine il ON t.TrackId = il.TrackId
	INNER join Invoice i ON il.InvoiceId = i.InvoiceId
	INNER JOIN Genre g ON t.GenreId=g.GenreId
	group by STRFTIME('%Y', i.InvoiceDate)
)

SELECT *,
	coalesce(round((VentasRock / TotalAnio) * 100,2),0.00) as PctCuotaRock
FROM GenreSales
ORDER by anio ASC
;