/*EnunciadoA partir de la tabla Invoice de la base de datos de la tienda, 
se requiere generar un informe analítico mensual que permita evaluar el 
desempeño de las ventas a lo largo del tiempo.Escribe una consulta SQL 
que devuelva una fila por cada mes con la siguiente información:
1. Mes (mes): Identificador del mes en formato YYYY-MM.
2. Ventas del Mes (VentasMes): La suma total del importe (total) facturado en dicho mes, 
redondeado a 2 decimales.
3. Ventas del Mes Anterior (VentasMesAnterior): El importe facturado en el 
mes previo mediante una función de ventana. Si no existe un mes anterior (primer registro), 
debe mostrar 0.
4. Crecimiento MoM (CrecimientoMoM): El porcentaje de variación intermensual (Month-over-Month) 
respecto al mes anterior, redondeado a 2 decimales, 
calculado mediante la fórmula: CrecimientoMoM = (VentasMes - VentasMesAnterior) / VentasMesAnterior * 100
5. Ventas Acumuladas (VentasAcumuladas): El total acumulado de ventas (running total) 
desde el primer mes hasta el mes actual, redondeado a 2 decimales.
*/

WITH VentasMes as (
	SELECT strftime('%Y-%m', InvoiceDate) AS mes,
	round(sum(total),2) as VentasMes
	FROM Invoice
	group by mes
	ORDER by mes ASC
	)

SELECT mes,
	VentasMes,
	LAG(VentasMes, 1, 0) OVER (ORDER BY mes ASC) as VentasMesAnterior,
	round((VentasMes-LAG(VentasMes, 1, 0) OVER (ORDER BY mes ASC))/LAG(VentasMes, 1, 0) OVER (ORDER BY mes ASC) *100,2) as CrecimientoMoM,
	round(SUM(VentasMes) OVER (ORDER BY mes ASC),2) as VentasAcumuladas
FROM VentasMes
ORDER by mes ASC

;