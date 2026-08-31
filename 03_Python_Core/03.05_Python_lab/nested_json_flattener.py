"""
PROBLEMA: APLANADO Y LIMPIEZA DE EVENTOS WEB ANIDADOS EN JSON (PYTHON NATIVO)

Trabajas en el pipeline de datos de una app. Recibes un archivo JSON ('eventos_raw.json') 
que contiene una lista de eventos de usuarios. La estructura del JSON es anidada y heterogénea:
algunos eventos vienen con la ubicación dividida, precios con moneda o metadatos nulos.

Entrada ('eventos_raw.json'):
[
    {
        "event_id": "evt_101",
        "user": {"id": "usr_99", "email": " ALICIA@EMAIL.COM "},
        "session": {
            "device": "mobile",
            "location": {"city": "Madrid", "country": "ES"}
        },
        "payload": {"action": "purchase", "amount_str": "120.50 EUR"},
        "timestamp": "2026-08-30T10:00:00"
    },
    {
        "event_id": "evt_102",
        "user": {"id": "usr_88", "email": "carlos_email.com"},
        "session": null,
        "payload": {"action": "click", "amount_str": "0 EUR"},
        "timestamp": "2026-08-30T10:05:00"
    },
    {
        "event_id": "evt_101",
        "user": {"id": "usr_99", "email": "alicia@email.com"},
        "session": {"device": "desktop", "location": null},
        "payload": {"action": "purchase", "amount_str": "120.50 EUR"},
        "timestamp": "2026-08-30T10:00:00"
    },
    {
        "event_id": "evt_103",
        "user": {"id": "usr_77", "email": "pedro@test.com"},
        "session": {
            "device": "tablet",
            "location": {"city": "Barcelona", "country": "ES"}
        },
        "payload": {"action": "purchase", "amount_str": "INVALID_AMOUNT"},
        "timestamp": "2026-08-30T10:10:00"
    }
]

Requisitos de Limpieza y Negocio:
1. Navegación Segura de Diccionarios Anidados:
   - Extrae 'user_id' y 'user_email'. Normaliza el email a minúsculas y sin espacios.
   - Si 'session' o 'location' es None/nulo, asigna "UNKNOWN" a la ciudad y país.
   - Si 'device' no está presente o es nulo, asigna "UNKNOWN".

2. Validaciones de Datos:
   - Descarta eventos con correos inválidos (sin '@', ej. evt_102).
   - Limpia 'amount_str' extrayendo el valor numérico a float (ej. "120.50 EUR" -> 120.50). 
     Si el valor no se puede convertir a float (ej. evt_103), descarta el evento.

3. Deduplicación por Clave Compuesta:
   - Descarta eventos duplicados basándote en la combinación ('event_id', 'user_id').

4. Estructura de Salida Aplanada (Tabla de Hechos):
   - Devuelve una lista de diccionarios con la estructura completamente aplanada (un solo nivel).

"""

import json

with open("eventos_raw.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

fact_table = []
eventos_vistos = set()

for d in datos:
    event_id = d["event_id"]
    user_id = d["user"]["id"]
    email = d["user"]["email"].strip().lower()

    # 1. Validación de Email
    if "@" not in email:
        continue

    # 2. Navegación Segura en Diccionarios Anidados (evita KeyError / AttributeError)
    session = d.get("session") or {}  # Si es None o no existe, usa {}
    device = session.get("device") or "UNKNOWN"

    location = session.get("location") or {}  # Extrae location de dentro de session
    city = location.get("city") or "UNKNOWN"
    country = location.get("country") or "UNKNOWN"

    # 3. Conversión de Importe
    action = d["payload"]["action"]
    amount_raw = d["payload"]["amount_str"].split(" ")[0].strip()
    try:
        amount = float(amount_raw)
    except ValueError:
        continue

    # 4. Deduplicación por Clave Compuesta
    clave_compuesta = (event_id, user_id)
    if clave_compuesta in eventos_vistos:
        continue

    # 5. Construcción de la Tabla de Hechos Aplanada
    eventos_vistos.add(clave_compuesta)
    fact_table.append({
        "event_id": event_id,
        "user_id": user_id,
        "user_email": email,
        "device": device,
        "city": city,
        "country": country,
        "action": action,
        "amount": amount,
        "timestamp": d["timestamp"]
    })

# Imprimir resultado
for registro in fact_table:
    print(registro)