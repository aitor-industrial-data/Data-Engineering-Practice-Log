#abrir archivo ventas.csv con pandas
import pandas as pd

ventas = pd.read_csv("ventas.csv")



#calcular cuanto suma la columa de unit_price por quantity
ventas["total"] = ventas["unit_price"] * ventas["quantity"]



#sumar la columna total
total_ventas = ventas["total"].sum()

#eliminar filas con product_category nulo
ventas = ventas.dropna(subset=["product_category"])