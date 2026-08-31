sesiones = [
    {"session_id": "s_10", "user_id": "u_01", "ip": "192.168.1.1", "login_time": "2026-08-31T08:00:00"},
    {"session_id": "s_20", "user_id": "u_02", "ip": "10.0.0.5", "login_time": "2026-08-31T08:15:00"},
    {"session_id": "s_30", "user_id": "u_03", "ip": "172.16.0.1", "login_time": "2026-08-31T08:30:00"},
    {"session_id": "s_30", "user_id": "u_01", "ip": "172.16.1.1", "login_time": "2026-08-31T08:30:00"},
]

transacciones = [
    {"tx_id": "t_101", "user_id": "u_01", "ip": "192.168.1.1", "amount": 150.0},
    {"tx_id": "t_102", "user_id": "u_02", "ip": "185.220.101.5", "amount": 999.0},
    {"tx_id": "t_103", "user_id": "u_04", "ip": "192.168.1.50", "amount": 45.0},
    {"tx_id": "t_104", "user_id": "u_01", "ip": "192.168.1.1", "amount": -20.0},
]

mapa_sesiones={s["user_id"]:s for s in sesiones}
for m in mapa_sesiones:
    print(m)
sesion = mapa_sesiones.get( "u_01")   
print(sesion)
report=[]
for t in transacciones:
    sesion = mapa_sesiones.get( t["user_id"] )   
    
    if sesion == None:
        r='unknow'
    elif t["ip"]==sesion["ip"]:
        r='same ip'
    else:
        r='diferent ip'
    
    line={
        "tx_id":t["tx_id"],
        "user_id":t["user_id"],
        "ip_t":t['ip'],
        "amount":t["amount"],
        'r':r
    }
    report.append(line)

for r in report:
    print(r)