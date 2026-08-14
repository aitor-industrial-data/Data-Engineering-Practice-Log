import csv


ingresos_categoria = {}
max_unidades = -1
producto_top = None

with open('productos.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for line in lector:
        line['unidades_vendidas']=float(line['unidades_vendidas'])
        if line['unidades_vendidas']>0:
            categoria = line['categoria']
            precio= float(line['precio'].replace('$',''))
            print(categoria, precio)
            
            ingresos_categoria[categoria] = ingresos_categoria.get(categoria, 0.0) + precio
            

    for cat, precio in ingresos_categoria.items():
        print(f'ingresos por categoria: {cat} ->> {precio}')