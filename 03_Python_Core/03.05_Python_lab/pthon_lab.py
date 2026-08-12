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
            
            
print(facturacion_region)
print(gastos_cliente)
# Buscar el cliente top iterando el diccionario
cliente_top = 'none' 
monto_top=0.0

for nombre,monto in gastos_cliente.items():
    monto=float(monto)
    if monto>monto_top:
        monto_top=monto
        cliente_top=nombre

print(f'el cliente top es {cliente_top} y su monto es {monto_top}$')
