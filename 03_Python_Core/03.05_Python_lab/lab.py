import csv
from datetime import datetime

with open("clientes_raw.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    
    data=[]
    for fila in lector:
        
        fila["nombre"]=fila["nombre"].strip().title()
        fila["email"]=fila["email"].strip().lower()
        fecha_clean = fila["fecha_registro"].strip()
        try:
            fecha_obj = datetime.strptime(fecha_clean, "%Y-%m-%d")
        except ValueError:
            fecha_obj = datetime.strptime(fecha_clean, "%d/%m/%Y")

        try:
            fila['gasto_total']=float(fila['gasto_total'])
        except ValueError:
            continue

        fila["fecha_registro"] = fecha_obj.strftime("%Y-%m-%d")
        
        if fila["nombre"] in {'',None} or '@' not in fila["email"]:
            continue
    
        data.append(fila)

        for dicc in data:
            if fila['id'] !=dicc['id']:
                print(dicc)
        
    #print(data)
    