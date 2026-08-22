"""
Enunciado:
Escribe un programa que procese tres entradas ingresadas por el usuario por consola:
1. Una lista de precios separados por comas.
2. Una lista de nombres de artículos separados por comas (mismo orden que los precios).
3. Un presupuesto máximo permitido por artículo.

El programa debe calcular e imprimir:
- La lista de artículos cuyo precio sea menor o igual al presupuesto individual (Can buy).
- El presupuesto total necesario para comprar únicamente esos artículos asequibles (Total budget needed).
- La cantidad total de artículos que superan el presupuesto y no se pueden comprar (Can't afford).

Ejemplo de entrada:
10,25,5,15
hammer,saw,nails,brush
12

Salida esperada:
Can buy: ['hammer', 'nails']
Total budget needed: 15
Can't afford: 2
"""

# Entradas por consola
prices = input().split(",")
for i in range(len(prices)):
    prices[i] = int(prices[i])
items = input().split(",")
budget_per_item = int(input())

affordable_items = []
cant_afford = 0
total_needed = 0

# Lógica del programa
for i in range(len(prices)):
    if prices[i] <= budget_per_item:
        affordable_items.append(items[i])
        total_needed += prices[i]
    else:
        cant_afford += 1

# Impresión de resultados
print("Can buy:", affordable_items)
print("Total budget needed:", total_needed)
print("Can't afford:", cant_afford)