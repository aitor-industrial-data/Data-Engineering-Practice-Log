"""
PROBLEMA: ENRIQUECIMIENTO DE PEDIDOS Y CATÁLOGO DE PRODUCTOS (JOIN & NULL HANDLING)

Trabajas en el pipeline de datos de un e-commerce. Recibes un CSV con los pedidos realizados 
('pedidos.csv') y necesitas enriquecerlo cruzando cada línea con la información completa 
del catálogo de productos ('productos.csv').

Entrada 1 ('productos.csv'):
product_id,nombre_producto,categoria,precio_unitario
p_10,Laptop Pro 15,Electronica,1200.00
p_20,Raton Inalambrico,Electronica,25.00
p_30,Teclado Mecanico,Electronica,80.00
p_40,Silla Ergonomica,Mobiliario,250.00

Entrada 2 ('pedidos.csv'):
order_id,user_id,product_id,cantidad,descuento_pct
ord_01,usr_100,p_10,1,0.10
ord_02,usr_200,p_20,2,0.00
ord_03,usr_100,p_99,1,0.00
ord_04,usr_300,p_30,-3,0.05
ord_05,usr_200,p_40,1,N/A

Requisitos de Limpieza y Negocio:
1. Indexación del Catálogo (Hash Join):
   - Carga 'productos.csv' e indéxalo en un diccionario por 'product_id' para hacer búsquedas O(1).
   - Convierte 'precio_unitario' a float.

2. Validaciones y Limpieza de Pedidos:
   - Convierte 'cantidad' a int. Descarta pedidos con 'cantidad' <= 0 (ej. ord_04).
   - Convierte 'descuento_pct' a float. Si no es numérico o es 'N/A' (ej. ord_05), asume un descuento de 0.00.

3. Enriquecimiento y Cálculo (LEFT JOIN):
   - Para cada pedido, busca el producto en el mapa del catálogo.
   - Si el 'product_id' NO existe en el catálogo (ej. p_99 en ord_03), asigna:
     * 'nombre_producto' = "DESCONOCIDO"
     * 'categoria' = "DESCONOCIDO"
     * 'total_linea' = 0.00
     * 'status_producto' = "PRODUCT_NOT_FOUND"
   - Si el producto EXISTE:
     * Calcula: total_linea = cantidad * precio_unitario * (1 - descuento_pct)
     * Redondea 'total_linea' a 2 decimales.
     * 'status_producto' = "OK"

4. Estructura de Salida:
   - Una lista de diccionarios con la información enriquecida del pedido.


"""
import csv 

lista_pedidos = []
mapa_productos = {}

# 1. Cargar e indexar el catálogo de productos (Hash Join)
with open("productos.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        mapa_productos[fila["product_id"]] = {
            "nombre_producto": fila["nombre_producto"],
            "categoria": fila["categoria"],
            "precio_unitario": float(fila["precio_unitario"])
        }

# 2. Procesar y enriquecer los pedidos
with open("pedidos.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)

    for f in lector:
        # Validar y convertir cantidad
        try:
            cantidad = int(f["cantidad"])
        except ValueError:
            continue

        if cantidad <= 0:
            continue

        # Validar y convertir descuento
        try:
            descuento_pct = float(f["descuento_pct"])
        except ValueError:
            descuento_pct = 0.00

        order_id = f["order_id"]
        user_id = f["user_id"]
        product_id = f["product_id"]

        # LEFT JOIN: Búsqueda segura usando .get()
        producto = mapa_productos.get(product_id)

        # Evaluación con .get()
        if producto is None:
            nombre_producto = "DESCONOCIDO"
            categoria = "DESCONOCIDO"
            total_linea = 0.00
            status_producto = "PRODUCT_NOT_FOUND"
        else:
            nombre_producto = producto["nombre_producto"]
            categoria = producto["categoria"]
            precio_unitario = producto["precio_unitario"]
            total_linea = round(cantidad * precio_unitario * (1 - descuento_pct), 2)
            status_producto = "OK"

        # Construcción del registro final
        pedido = {
            "order_id": order_id,
            "user_id": user_id,
            "product_id": product_id,
            "nombre_producto": nombre_producto,
            "categoria": categoria,
            "cantidad": cantidad,
            "descuento_pct": descuento_pct,
            "total_linea": total_linea,
            "status_producto": status_producto
        }

        lista_pedidos.append(pedido)

for l in lista_pedidos:
    print(l)