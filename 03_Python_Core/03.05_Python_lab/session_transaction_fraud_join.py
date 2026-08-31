"""
PROBLEMA: CORRELACIÓN DE EVENTOS DE SESIÓN Y TRANSACCIONES (JOIN & DATA QUALITY)

Trabajas en el pipeline de ciberseguridad y fraude. Tienes dos fuentes de datos en formato de listas de diccionarios:
1. 'sesiones': Inicios de sesión de usuarios con su IP y timestamp.
2. 'transacciones': Compras realizadas por usuarios con su IP y timestamp.

Debes cruzar (JOIN) ambas fuentes por 'user_id' para validar si la compra se realizó desde la MISMA IP 
con la que el usuario inició sesión, y detectar transacciones sospechosas (IPs distintas o sin sesión previa).

Datos de entrada (simulados en el script):

sesiones = [
    {"session_id": "s_10", "user_id": "u_01", "ip": "192.168.1.1", "login_time": "2026-08-31T08:00:00"},
    {"session_id": "s_20", "user_id": "u_02", "ip": "10.0.0.5", "login_time": "2026-08-31T08:15:00"},
    {"session_id": "s_30", "user_id": "u_03", "ip": "172.16.0.1", "login_time": "2026-08-31T08:30:00"},
]

transacciones = [
    {"tx_id": "t_101", "user_id": "u_01", "ip": "192.168.1.1", "amount": 150.0},  # Coincide IP
    {"tx_id": "t_102", "user_id": "u_02", "ip": "185.220.101.5", "amount": 999.0}, # IP DISTINTA -> SOSPECHOSO
    {"tx_id": "t_103", "user_id": "u_04", "ip": "192.168.1.50", "amount": 45.0},  # Sin sesión -> SOSPECHOSO
    {"tx_id": "t_104", "user_id": "u_01", "ip": "192.168.1.1", "amount": -20.0},  # Monto inválido
]

Requisitos de Limpieza y Negocio:
1. Filtrado Previos:
   - Descarta transacciones con 'amount' <= 0 (ej. t_104).

2. Cruzado de Datos (LEFT JOIN):
   - Mapea las sesiones por 'user_id' para una búsqueda rápida O(1).
   - Para cada transacción válida, busca la sesión del usuario.

3. Reglas de Clasificación de Riesgo:
   - Si el usuario NO tiene sesión registrada: 'risk_level' = "HIGH_NO_SESSION".
   - Si el usuario tiene sesión PERO la 'ip' de la transacción NO coincide con la de la sesión: 
     'risk_level' = "HIGH_IP_MISMATCH".
   - Si la 'ip' coincide exactamente: 'risk_level' = "LOW".

4. Estructura de Salida:
   - Devuelve una lista de diccionarios con la información enriquecida de la transacción.

"""
sesiones = [
    {"session_id": "s_10", "user_id": "u_01", "ip": "192.168.1.1", "login_time": "2026-08-31T08:00:00"},
    {"session_id": "s_20", "user_id": "u_02", "ip": "10.0.0.5", "login_time": "2026-08-31T08:15:00"},
    {"session_id": "s_30", "user_id": "u_03", "ip": "172.16.0.1", "login_time": "2026-08-31T08:30:00"},
]

transacciones = [
    {"tx_id": "t_101", "user_id": "u_01", "ip": "192.168.1.1", "amount": 150.0},  # Coincide IP
    {"tx_id": "t_102", "user_id": "u_02", "ip": "185.220.101.5", "amount": 999.0}, # IP DISTINTA -> SOSPECHOSO
    {"tx_id": "t_103", "user_id": "u_04", "ip": "192.168.1.50", "amount": 45.0},  # Sin sesión -> SOSPECHOSO
    {"tx_id": "t_104", "user_id": "u_01", "ip": "192.168.1.1", "amount": -20.0},  # Monto inválido
]

sesiones = [
    {"session_id": "s_10", "user_id": "u_01", "ip": "192.168.1.1", "login_time": "2026-08-31T08:00:00"},
    {"session_id": "s_20", "user_id": "u_02", "ip": "10.0.0.5", "login_time": "2026-08-31T08:15:00"},
    {"session_id": "s_30", "user_id": "u_03", "ip": "172.16.0.1", "login_time": "2026-08-31T08:30:00"},
]

transacciones = [
    {"tx_id": "t_101", "user_id": "u_01", "ip": "192.168.1.1", "amount": 150.0},
    {"tx_id": "t_102", "user_id": "u_02", "ip": "185.220.101.5", "amount": 999.0},
    {"tx_id": "t_103", "user_id": "u_04", "ip": "192.168.1.50", "amount": 45.0},
    {"tx_id": "t_104", "user_id": "u_01", "ip": "192.168.1.1", "amount": -20.0},
]

# PASO 1: Mapear sesiones por user_id (Búsqueda instantánea O(1))
mapa_sesiones = {s["user_id"]: s for s in sesiones}

report = []

# PASO 2: Procesar transacciones
for t in transacciones:
    try:
        amount = float(t["amount"])
    except ValueError:
        continue

    if amount <= 0:
        continue

    tx_id = t["tx_id"]
    user_id_t = t["user_id"]
    ip_t = t["ip"]

    # Búsqueda directa del usuario en el mapa
    sesion = mapa_sesiones.get(user_id_t)

    # Evaluación de la lógica de negocio
    if not sesion:
        ip_s = "UNKNOWN"
        risk_level = "HIGH_NO_SESSION"
    elif sesion["ip"] != ip_t:
        ip_s = sesion["ip"]
        risk_level = "HIGH_IP_MISMATCH"
    else:
        ip_s = sesion["ip"]
        risk_level = "LOW"

    linea = {
        "tx_id": tx_id,
        "user_id": user_id_t,
        "amount": amount,
        "ip_tx": ip_t,
        "ip_session": ip_s,
        "risk_level": risk_level
    }
    report.append(linea)

for r in report:
    print(r)