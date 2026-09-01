"""
PROBLEMA: MÉTRICAS DE CLIENTE Y SEGMENTACIÓN RFM SIMPLIFICADA (GROUP BY & AGGREGATION)

Trabajas en el departamento de Analytics de una plataforma digital. Tienes una lista de 
transacciones de usuarios ('actividad_clientes.csv') y debes generar un informe analítico 
por cliente para identificar a los usuarios más valiosos (VIPs) y detectar a los inactivos.

Entrada ('actividad_clientes.csv'):
user_id,monto,categoria,fecha
usr_100,150.00,Suscripcion,2026-08-01
usr_200,45.50,Tienda,2026-08-03
usr_100,200.00,Tienda,2026-08-15
usr_300,-10.00,Tienda,2026-08-16
usr_200,N/A,Suscripcion,2026-08-20
usr_100,50.00,Tienda,2026-08-28
usr_400,300.00,Tienda,2026-08-29

Requisitos de Limpieza y Negocio:
1. Filtrado y Validación:
   - Limpia 'monto' convirtiéndolo a float. Descarta registros con 'monto' <= 0 o no numéricos ('N/A').

2. Agregación por Cliente (GROUP BY user_id):
   Para cada cliente válido, calcula:
   - 'total_gastado': Suma de los montos gastados (redondeado a 2 decimales).
   - 'num_transacciones': Cantidad de compras válidas realizadas.
   - 'ticket_medio': Promedio gastado por transacción (total_gastado / num_transacciones), redondeado a 2 decimales.
   - 'categorias_usadas': Lista o conjunto de categorías ÚNICAS en las que ha comprado.

3. Clasificación de Segmento:
   - Si 'total_gastado' >= 300.00 -> 'segmento' = "VIP"
   - Si 'total_gastado' < 300.00 -> 'segmento' = "ESTÁNDAR"

4. Ordenación Final:
   - Devuelve la lista final de clientes ordenada de MAYOR a MENOR según su 'total_gastado'.

"""
import csv

clientes = {}

# 1. Bucle de Agregación (Acumular datos en bruto)
with open("actividad_clientes.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        # Validación numérica
        try:
            monto = float(fila["monto"])
        except ValueError:
            continue

        if monto <= 0:
            continue

        user_id = fila["user_id"]
        categoria = fila["categoria"]

        # Inicializar estructura si el cliente no existe
        if user_id not in clientes:
            clientes[user_id] = {
                "total_gastado": 0.0,
                "num_transacciones": 0,
                "categorias_usadas": set()  # Set individual por cliente
            }

        # Acumular valores
        clientes[user_id]["total_gastado"] += monto
        clientes[user_id]["num_transacciones"] += 1
        clientes[user_id]["categorias_usadas"].add(categoria)

# 2. Bucle de Transformación (Calcular métricas derivadas)
report = []

for user_id, datos in clientes.items():
    total_gastado = round(datos["total_gastado"], 2)
    num_transacciones = datos["num_transacciones"]
    ticket_medio = round(total_gastado / num_transacciones, 2)
    segmento = "VIP" if total_gastado >= 300.0 else "ESTÁNDAR"

    report.append({
        "user_id": user_id,
        "total_gastado": total_gastado,
        "num_transacciones": num_transacciones,
        "ticket_medio": ticket_medio,
        "categorias_usadas": list(datos["categorias_usadas"]),  # Convertir set a list
        "segmento": segmento
    })

# 3. Ordenación final por gasto de MAYOR a MENOR
report_ordenado = sorted(report, key=lambda x: x["total_gastado"], reverse=True)

# Imprimir resultado
for r in report_ordenado:
    print(r)