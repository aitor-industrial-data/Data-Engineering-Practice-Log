"""
PROBLEMA: RECONCILIACIÓN Y AUDITORÍA DE INVENTARIO MULTI-ALMACÉN (PYTHON NATIVO)

Trabajas como Data Engineer en una empresa de logística. Recibes un archivo CSV en bruto 
'inventario_raw.csv' que consolida el stock de diferentes almacenes. 
El archivo contiene inconsistencias: códigos de producto mal formateados, cantidades negativas 
o corruptas, nombres de almacén duplicados por espacios/mayúsculas y registros inconsistentes.

Entrada ('inventario_raw.csv'):
sku,almacen,monto_unitario,stock,estado
PROD-001,  Madrid_Central ,25.50,100,DISPONIBLE
prod-001,madrid_central,25.50,50,DISPONIBLE
PROD-002,BARCELONA_NORTH,12.00,-5,DISPONIBLE
PROD-003, Valencia_East ,N/A,30,DISPONIBLE
PROD-004, Madrid_Central ,45.00,20,DESCONTINUADO
PROD-005,BARCELONA_NORTH,80.00,15,disponible

Requisitos de Limpieza y Negocio:
1. Normalización de Cadenas:
   - El campo 'sku' debe estar completamente en MAYÚSCULAS y sin espacios sobrantes.
   - El campo 'almacen' debe estar en MINÚSCULAS, sin espacios sobrantes y reemplazando 
     los espacios internos por guiones bajos (ej. ' Madrid_Central ' -> 'madrid_central').
   - El campo 'estado' debe estar en MAYÚSCULAS.

2. Validación y Filtrado de Filas:
   - Descarta registros con 'estado' diferente de 'DISPONIBLE' (ej. PROD-004).
   - Descarta registros con 'stock' menor o igual a 0 (ej. PROD-002).
   - Convertir 'monto_unitario' a float y 'stock' a int. Si 'monto_unitario' no es numérico 
     (ej. 'N/A' en PROD-003), descarta la fila.

3. Consolidador y Agregación (GROUP BY):
   - Agrupa los datos por 'almacen' y calcula:
     a) 'valor_total_inventario': Suma de (stock * monto_unitario) para ese almacén.
     b) 'total_unidades': Suma de las unidades de stock.
     c) 'skus_unicos': Lista o conjunto con los SKUs únicos presentes en dicho almacén.

"""

import csv

resumen_almacenes = {}

with open("inventario_raw.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)

    for line in lector:
        # 1. Normalización de cadenas
        sku = line["sku"].strip().upper()
        almacen = line["almacen"].strip().lower().replace(" ", "_")
        estado = line["estado"].strip().upper()

        # 2. Filtrado por estado
        if estado != "DISPONIBLE":
            continue

        # 3. Conversión numérica y validación de tipos
        try:
            monto_unitario = float(line["monto_unitario"].strip())
            stock = int(line["stock"].strip())
        except ValueError:
            continue

        # 4. Filtrado por cantidad
        if stock <= 0:
            continue

        # 5. Inicialización del almacén si no existe
        if almacen not in resumen_almacenes:
            resumen_almacenes[almacen] = {
                "valor_total_inventario": 0.0,
                "total_unidades": 0,
                "skus_unicos": set()  # Set individual por almacén
            }

        # 6. Agregación acumulativa directa
        resumen_almacenes[almacen]["valor_total_inventario"] += stock * monto_unitario
        resumen_almacenes[almacen]["total_unidades"] += stock
        resumen_almacenes[almacen]["skus_unicos"].add(sku)

# Opcional: Convertir los sets a listas si se va a exportar a JSON/dict final
for datos in resumen_almacenes.values():
    datos["skus_unicos"] = list(datos["skus_unicos"])
    datos["valor_total_inventario"] = round(datos["valor_total_inventario"], 2)

print(resumen_almacenes)