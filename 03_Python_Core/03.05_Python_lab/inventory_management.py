"""
Nombre de archivo recomendado: inventory_management.py

ENUNCIADO DEL PROBLEMA: Sistema de Gestión de Inventario y Ventas

Crea un script en Python que permita administrar el inventario de una tienda utilizando 
un diccionario global. El sistema debe implementar las siguientes funcionalidades:

1. add_item(item, price, stock):
   Registra un nuevo producto con su precio y stock inicial. Si el producto ya existe,
   debe mostrar un mensaje de error sin modificar los datos.

2. update_stock(item, quantity):
   Añade o descuenta unidades al stock de un producto existente. Debe validar que el
   producto exista en el inventario y que el resultado final no sea menor a cero.

3. check_availability(item):
   Consulta y retorna la cantidad disponible de un producto. Si el producto no existe,
   retorna el mensaje "Item not found".

4. sales_report(sales):
   Recibe un diccionario con las ventas a realizar (clave: nombre del producto, valor: cantidad).
   Para cada fila de venta, valida que el producto exista y cuente con stock suficiente. 
   Descuenta las unidades vendidas, acumula el importe total de las ventas válidas e 
   imprime mensajes de error para aquellos artículos sin stock o no registrados.
   Devuelve un string con el total recaudado formateado a dos decimales.

Caso de prueba básico:
- Registrar "Apple" ($0.50, stock: 50) y "Banana" ($0.20, stock: 60).
- Procesar ventas: {"Apple": 30, "Banana": 20, "Orange": 10}.
- Salida esperada del reporte: "Total revenue: $19.00"
"""


inventory={}


def add_item (item:str,price:float,stock:int):
    if item in inventory:
        print(f"Error: Item '{item}' already exists.")
    else:
        inventory[item]={'price':price,
                        'stock':stock
                        }
        print(f"Item '{item}' added successfully.")


def update_stock(item:str, quantity:int):
    if item not in inventory:
        print(f"Error: Item '{item}' not found.")
    else:
        new_stock=inventory[item]['stock']+quantity
        if new_stock <0:
            print(f"Error: Insufficient stock for '{item}'.")
        else:
            inventory[item]['stock']=new_stock 
            print(f"Stock for '{item}' updated successfully.")



def check_availability(item:str):
    if item not in inventory:
        return "Item not found"
    else:
        return inventory[item]['stock']


def sales_report(sales:dict):
    total=0
    for item, value in sales.items():
        if item in inventory:
            if value <= inventory[item]['stock']:
                inventory[item]['stock']-=value
                total+= value*inventory[item]['price']
                
            else:
                 print (f"Error: Insufficient stock for '{item}'.")
        else:
            print (f"Error: Item '{item}' not found.")
        
    return (f'Total revenue: ${total:.2f}')

add_item("Apple", 0.5, 50)
add_item("Banana", 0.2, 60)
sales = {"Apple": 30, "Banana": 20, "Orange": 10}  # Orange should print an error
print(sales_report(sales))  # Should output: Total revenue: $19.00
print(inventory)