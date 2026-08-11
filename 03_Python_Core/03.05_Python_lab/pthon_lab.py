#abrir archivo ventas.csv con pandas
import pandas as pd

ventas = pd.read_csv("ventas.csv")



#calcular cuanto suma la columa de unit_price por quantity
ventas["total"] = ventas["unit_price"] * ventas["quantity"]

# Si total > 1000 pone 'VIP', si no pone 'NORMAL'
ventas["status"] = ["VIP" if total > 1000 else "NORMAL" for total in ventas["total"]]
print(ventas)