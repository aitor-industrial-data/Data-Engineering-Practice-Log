"""
PROBLEMA DE LIMPIEZA DE DATOS EN PYTHON NATIVO:

Recibes un archivo CSV en bruto ('clientes_raw.csv') generado por un sistema antiguo. 
El archivo contiene información de registros de usuarios, pero viene con espacio en blanco 
de más, fechas en formatos inconsistentes, correos mal formados y registros duplicados.

Archivo de entrada esperado ('clientes_raw.csv'):
id,nombre,email,fecha_registro,gasto_total
101,  juan pérez ,juan.perez@email.com,2026-01-15,150.50
102,MARIA GOMEZ,maria.gomez@DOMINIO.COM,15/02/2026,200.00
101,Juan Pérez,juan.perez@email.com,2026-01-15,150.50
103, carlos lopez ,carlos.lopez_email.com,2026-03-10,N/A
104,Ana TORRES,ana.torres@email.com,2026-04-01,95.00
105,  ,sin_email@domain.com,2026-04-05,0

Requisitos de Limpieza:
1. Formatos de Texto: 
   - Elimina espacios sobrantes al inicio y final de los campos 'nombre' y 'email'.
   - Normaliza los nombres para que tengan formato de título (ej. 'Juan Pérez').
   - Convierte todos los correos a minúsculas.

2. Validación de Datos:
   - Descarta cualquier fila que tenga el nombre en blanco o que no tenga un '@' válido en el email.

3. Estandarización de Fechas:
   - Detecta y convierte todas las fechas al formato estándar 'YYYY-MM-DD' (soportando 'YYYY-MM-DD' y 'DD/MM/YYYY').

4. Tratamiento de Números:
   - Convierte 'gasto_total' a tipo float. Si el valor es indeterminado (como 'N/A'), la fila debe ser descartada.

5. Deduplicación:
   - Elimina filas duplicadas basándote únicamente en el 'id'.
"""

import csv
from datetime import datetime

data = []
ids_procesados = set()  # Para deduplicar por ID eficientemente

with open("clientes_raw.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    
    for fila in lector:
        # 1. Limpieza de texto
        nombre = fila["nombre"].strip().title()
        email = fila["email"].strip().lower()
        cliente_id = fila["id"].strip()
        
        # 2. Validación de presencia y formato básico
        if not nombre or "@" not in email:
            continue
            
        # 3. Deduplicación por ID
        if cliente_id in ids_procesados:
            continue
            
        # 4. Normalización de fechas
        fecha_str = fila["fecha_registro"].strip()
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            try:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
            except ValueError:
                continue  # Si la fecha no cumple ningún formato
                
        # 5. Conversión numérica
        try:
            gasto = float(fila["gasto_total"])
        except ValueError:
            continue

        # Registro limpio final
        registro_limpio = {
            "id": int(cliente_id),
            "nombre": nombre,
            "email": email,
            "fecha_registro": fecha_obj.strftime("%Y-%m-%d"),
            "gasto_total": gasto
        }
        
        data.append(registro_limpio)
        ids_procesados.add(cliente_id)

print(data)