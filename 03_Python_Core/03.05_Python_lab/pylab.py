"""prices = input().split(",")
for i in range(len(prices)):
    prices[i] = int(prices[i])
items = input().split(",")
budget_per_item = int(input())"""

affordable_items = []
cant_afford = 0
total_needed = 0


# Escribe tu código debajo
prices=[10,25,5,15]
items=['hammer','saw','nails','brush']
budget_per_item=12



for i in range(len(prices)):
    if prices[i]<budget_per_item:
        affordable_items.append(items[i])
        total_needed+=prices[i]
    else:
        cant_afford+=1

print("Can buy:", affordable_items)
print("Total budget needed:", total_needed)
print("Can't afford:", cant_afford)
