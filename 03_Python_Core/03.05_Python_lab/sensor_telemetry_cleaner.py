"""
PROBLEMA: PROCESAMIENTO Y LIMPIEZA DE SENSOR LOGS INDUSTRIALES (PYTHON NATIVO)

Trabajas en el equipo de IoT/Telemetría de una planta industrial. Recibes un archivo 
de texto plano ('sensores_raw.txt') donde cada línea es un evento enviado por sensores 
de temperatura. Muchas líneas están corruptas por fallos en la red o contienen lecturas 
duplicadas generadas por reintentos de los dispositivos.

Entrada ('sensores_raw.txt'):
[2026-08-30 08:00:00] SENSOR_ID=S-01 | TEMP=45.2C | STATUS=OK
[2026-08-30 08:00:00] SENSOR_ID=S-01 | TEMP=45.2C | STATUS=OK
[2026-08-30 08:01:15] SENSOR_ID=s-02 | TEMP=ERROR | STATUS=FAIL
[2026-08-30 08:02:10] SENSOR_ID=S-01 | TEMP=88.5C | STATUS=CRITICAL
[2026-08-30 08:03:00] SENSOR_ID=S-03 | TEMP=32.0C | STATUS=OK
[2026-08-30 08:03:45] SENSOR_ID=S-02 | TEMP=105.0C | STATUS=OVERHEAT
CORRUPTED_LINE_WITHOUT_FORMAT_####
[2026-08-30 08:04:12] SENSOR_ID=S-01 | TEMP=46.1C | STATUS=OK

Requisitos de Limpieza y Negocio:
1. Parseo y Extracción de Campos:
   - Extrae el timestamp, el sensor_id, la temperatura numérica y el estatus.
   - Si una línea no cumple con el formato exacto de separadores ('|') o falta información, descártala.

2. Normalización de Cadenas:
   - El 'sensor_id' debe estar en MAYÚSCULAS (ej. 's-02' -> 'S-02').
   - El 'status' debe estar en MAYÚSCULAS.

3. Validaciones Numéricas y Filtrado:
   - Extrae el valor numérico flotante de 'TEMP' eliminando el sufijo 'C' (ej. '45.2C' -> 45.2).
   - Descarta cualquier registro donde la lectura de temperatura contenga palabras como 'ERROR' 
     o no sea un número válido.

4. Deduplicación Estricta:
   - Si existen dos lecturas para el MISMO 'sensor_id' en el MISMO 'timestamp' (segundo exacto), 
     conserva solo la primera ocurrencia y descarta la repetida.

5. Estructura de Salida:
   - Devuelve una lista de diccionarios limpios ordenados cronológicamente por timestamp.

"""
sensores_clean = []
registros_vistos = set()  # Guarda tuplas (sensor_id, timestamp) para deduplicar en O(1)

with open("sensores_raw.txt", "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        
        try:
            # 1. Separar los 3 bloques principales
            log, temp_raw, status_raw = linea.split('|')
            
            # 2. Parsear fecha y sensor
            timestamp_raw, sensor_raw = log.split("]")
            timestamp = timestamp_raw.strip("[").strip()
            sensor_id = sensor_raw.split("=")[1].strip().upper()
            
            # 3. Parsear temperatura (eliminar 'C' y convertir a float)
            temp_str = temp_raw.split("=")[1].replace("C", "").strip()
            temperatura = float(temp_str)
            
            # 4. Parsear estatus
            status = status_raw.split("=")[1].strip().upper()

        except (ValueError, IndexError):
            # Captura líneas con formato incorrecto o errores de conversión a float
            continue

        # 5. Deduplicación estricta por (sensor_id, timestamp)
        clave_unica = (sensor_id, timestamp)
        if clave_unica in registros_vistos:
            continue

        # Registrar la ocurrencia
        registros_vistos.add(clave_unica)
        sensores_clean.append({
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "temperatura": temperatura,
            "status": status
        })

# Imprimir resultado
for registro in sensores_clean:
    print(registro)