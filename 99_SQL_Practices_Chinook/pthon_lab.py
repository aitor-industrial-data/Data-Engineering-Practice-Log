raw_logs = [
    {"timestamp": "2026-08-10 10:00:00", "endpoint": "/api/v1/users", "status_code": "200", "response_ms": 120},
    {"timestamp": "2026-08-10 10:01:00", "endpoint": "/api/v1/orders", "status_code": 200, "response_ms": 250},
    {"timestamp": "2026-08-10 10:01:15", "endpoint": "/api/v1/users", "status_code": 500, "response_ms": 450},
    {"timestamp": "2026-08-10 10:02:00", "endpoint": None, "status_code": 404, "response_ms": 80},  # ❌ Registro corrupto (endpoint None)
    {"timestamp": "2026-08-10 10:02:30", "endpoint": "/api/v1/orders", "status_code": "503", "response_ms": "300"},
    {"timestamp": "2026-08-10 10:03:00", "endpoint": "/api/v1/users", "status_code": 200, "response_ms": None}, # ❌ Registro corrupto (response_ms None)
    {"timestamp": "2026-08-10 10:03:45", "endpoint": "/api/v1/orders", "status_code": 200, "response_ms": 210},
]

clean_logs = []

for log in raw_logs:
    if log["endpoint"] is None:
        print(f'{log} ❌ Registro corrupto (endpoint None)')
    if log['response_ms'] is None:
        print(f'{log} ❌ Registro corrupto (response_ms None)')
    else:
        clean_logs.append(log)

result={}
max_ms=0
for log in clean_logs:
    ms=int(log["status_code"])
    if ms>max_ms:
        max_ms=ms
        result=log
print(raw_logs[1])
print('#################################')
print (f' max response_ms es: {result}')