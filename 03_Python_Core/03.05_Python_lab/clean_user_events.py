"""
RETO: Depuración y Enriquecimiento de Eventos de Usuarios

DESCRIPCIÓN:
Recibes un flujo de registros de eventos de una aplicación en formato de 
lista de diccionarios (logs_raw). Algunos registros contienen duplicados exactos,
otros tienen eventos nulos (None) y necesitas procesarlos para clasificar 
a los usuarios según su actividad.

DATOS DE ENTRADA:
logs_raw = [
    {"user_id": 101, "event": "login", "timestamp": "10:00"},
    {"user_id": 102, "event": "click", "timestamp": "10:02"},
    {"user_id": 101, "event": "click", "timestamp": "10:05"},
    {"user_id": 103, "event": "login", "timestamp": "10:06"},
    {"user_id": 101, "event": "login", "timestamp": "10:00"},  # Duplicado exacto
    {"user_id": 104, "event": None, "timestamp": "10:10"},     # Evento inválido
    {"user_id": 102, "event": "purchase", "timestamp": "10:12"},
    {"user_id": 105, "event": "click", "timestamp": "10:15"}
]

CRITICAL_EVENTS = ("login", "purchase")

REQUISITOS:
1. Filtrar registros no válidos: Ignorar cualquier registro cuyo "event" sea None.
2. Eliminar duplicados exactos: Evitar procesar registros idénticos manteniendo 
   el orden de llegada original.
3. Identificar usuarios críticos: Guardar en un SET los user_id que hayan 
   realizado al menos un evento presente en la tupla CRITICAL_EVENTS.
4. Agrupar eventos por usuario: Construir un DICCIONARIO donde la clave sea 
   el user_id y el valor sea una LISTA con su secuencia de eventos válidos.

SALIDA ESPERADA:
- Usuarios críticos (set): {101, 102, 103}
- Historial por usuario (dict): {
    101: ['login', 'click'],
    102: ['click', 'purchase'],
    103: ['login'],
    105: ['click']
  }
"""

logs_raw = [
    {"user_id": 101, "event": "login", "timestamp": "10:00"},
    {"user_id": 102, "event": "click", "timestamp": "10:02"},
    {"user_id": 101, "event": "click", "timestamp": "10:05"},
    {"user_id": 103, "event": "login", "timestamp": "10:06"},
    {"user_id": 101, "event": "login", "timestamp": "10:00"},  # Duplicado exacto
    {"user_id": 104, "event": None, "timestamp": "10:10"},     # Evento inválido
    {"user_id": 102, "event": "purchase", "timestamp": "10:12"},
    {"user_id": 105, "event": "click", "timestamp": "10:15"}
]

CRITICAL_EVENTS = ("login", "purchase")

seen_logs = set()
critical_users = set()
user_events = {}

for log in logs_raw:
    user_id = log["user_id"]
    event = log["event"]
    timestamp = log["timestamp"]
    
    # 1. Descartar None
    if event is None:
        continue
        
    # 2. Descartar duplicados exactos en O(1) manteniendo el orden original
    log_tuple = (user_id, event, timestamp)
    if log_tuple in seen_logs:
        continue
    seen_logs.add(log_tuple)
    
    # 3. Detectar usuarios con eventos críticos
    if event in CRITICAL_EVENTS:
        critical_users.add(user_id)
        
    # 4. Agrupar eventos en lista por usuario
    if user_id not in user_events:
        user_events[user_id] = []
    user_events[user_id].append(event)

print("Usuarios críticos (Set):", critical_users)
print("Eventos por usuario (Dict):", user_events)