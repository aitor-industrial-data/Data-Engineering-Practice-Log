import csv
from collections import defaultdict

# Diccionarios acumuladores
facturacion_region = defaultdict(float)
gastos_cliente = defaultdict(float)

with open('pedidos.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        # 1. Filtrar solo completados
        if fila['estado'] == 'Completado':
            region = fila['region']
            cliente = fila['cliente']
            monto = float(fila['monto_eur'])
            
            # 2 y 3. Acumular totales
            facturacion_region[region] += monto
            gastos_cliente[cliente] += monto

# Buscar el cliente top iterando el diccionario
cliente_top = max(gastos_cliente, key=gastos_cliente.get)
monto_top = gastos_cliente[cliente_top]

print("--- Facturación por Región (Completados) ---")
for region, total in facturacion_region.items():
    print(f"{region}: {total:.2f} €")

print("\n--- Cliente Top ---")
print(f"El cliente con más gasto es {cliente_top} con {monto_top:.2f} €")