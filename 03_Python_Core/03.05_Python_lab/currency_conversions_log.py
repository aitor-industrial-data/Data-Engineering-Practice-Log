"""
PROBLEMA: PROCESAMIENTO Y CRUCE DE LOGS DE TRANSACCIONES (PYTHON NATIVO)

Trabajas en una plataforma e-commerce y recibes diariamente dos archivos de sistemas distintos:
1. 'ventas.csv': Registro de transacciones con montos en distintas monedas.
2. 'tasas_cambio.json': Un objeto JSON con las tasas de cambio del día a EUR (Euro).

El objetivo es calcular el total neto gastado por cada cliente convertidos a EUR, 
descartando transacciones inválidas o sospechosas.

Entrada 1 ('ventas.csv'):
id_transaccion,id_cliente,monto,moneda,fecha_utc
tx_01,usr_10,120.50,USD,2026-08-01T10:15:30
tx_02,usr_20,85.00,EUR,2026-08-01T11:00:00
tx_03,usr_10,-15.00,USD,2026-08-01T12:30:00
tx_04,usr_30,500.00,JPY,2026-08-01T13:45:00
tx_05,usr_20,100.00,GBP,2026-08-01T14:20:00
tx_06,usr_10,45.00,CAD,2026-08-01T15:10:00

Entrada 2 ('tasas_cambio.json'):
{
    "EUR": 1.0,
    "USD": 0.92,
    "GBP": 1.17,
    "JPY": 0.0061
}

Requisitos de Limpieza y Negocio:
1. Validación de Monto:
   - Descarta cualquier transacción cuyo monto sea menor o igual a 0 (ej. tx_03).

2. Conversión de Moneda:
   - Aplica la conversión correspondiente multiplying: monto_eur = monto * tasa.
   - Si la moneda de la transacción NO existe en el JSON de tasas (ej. CAD en tx_06), 
     la transacción debe ser descartada.
   - Redondea los valores finales en EUR a 2 decimales.

3. Formato de Fecha:
   - Procesa la fecha ISO (`YYYY-MM-DDTHH:MM:SS`) a un objeto datetime nativo. 
   - Ignora registros cuya fecha no tenga el formato correcto.

4. Agregación Final:
   - Genera una estructura final (diccionario) con la suma total gastada en EUR 
     y la cantidad de transacciones válidas por cada `id_cliente`.

"""

import csv
import json
from datetime import datetime

# 1. Cargar tasas de cambio
with open("tasas_cambio.json", "r", encoding="utf-8") as f:
    tasas = json.load(f)

resumen_clientes = {}

# 2. Leer y procesar transacciones
with open("ventas.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        try:
            monto = float(fila["monto"])
            if monto <= 0:
                continue

            moneda = fila["moneda"].strip()
            # Si la moneda no está en el JSON, lanzará KeyError y saltará al except
            tasa = tasas[moneda]

            # Validar formato ISO de fecha (si falla, lanza ValueError)
            datetime.fromisoformat(fila["fecha_utc"].strip())

            # Cálculo de monto en EUR
            monto_eur = monto * tasa
            cliente = fila["id_cliente"].strip()

            # 3. Agregación directa en el diccionario
            if cliente not in resumen_clientes:
                resumen_clientes[cliente] = {
                    "total_eur": 0.0,
                    "transacciones": 0
                }

            resumen_clientes[cliente]["total_eur"] += monto_eur
            resumen_clientes[cliente]["transacciones"] += 1

        except (ValueError, KeyError):
            # Captura montos/fechas inválidos (ValueError) o monedas inexistentes (KeyError)
            continue

# 4. Redondeo final para evitar imprecisiones de flotantes acumulados
for datos in resumen_clientes.values():
    datos["total_eur"] = round(datos["total_eur"], 2)

print(resumen_clientes)