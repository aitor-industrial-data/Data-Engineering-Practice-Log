# 📘 Python Datasheet — Bucles (for, while, comprehensions)

---

## 🔹 `for` — sintaxis básica

```python
for elemento in iterable:
    # bloque
```

```python
for valor in [10, 20, 30]:
    print(valor)

for letra in "abc":
    print(letra)

for i in range(5):          # 0,1,2,3,4
    print(i)

for i in range(2, 10, 2):    # inicio, fin (excl), paso -> 2,4,6,8
    print(i)
```

---

## 🔹 `range()` — resumen

| Sintaxis | Genera |
|---|---|
| `range(5)` | `0,1,2,3,4` |
| `range(2, 8)` | `2,3,4,5,6,7` |
| `range(0, 10, 2)` | `0,2,4,6,8` |
| `range(10, 0, -1)` | `10,9,...,1` (descendente) |

```python
list(range(5))          # [0, 1, 2, 3, 4]  -> range es un generador, hay que convertirlo
```

---

## 🔹 `enumerate()` — índice + valor

```python
sensores = ["T-101", "T-102", "T-103"]

for i, nombre in enumerate(sensores):
    print(i, nombre)
# 0 T-101
# 1 T-102
# 2 T-103

for i, nombre in enumerate(sensores, start=1):    # empezar en 1
    print(i, nombre)
```

---

## 🔹 `zip()` — recorrer varias colecciones a la vez

```python
nombres = ["T-101", "T-102", "T-103"]
temps = [76.4, 45.1, 90.0]

for nombre, temp in zip(nombres, temps):
    print(f"{nombre}: {temp}°C")

# zip se corta al iterable más corto
list(zip([1,2,3], [1,2]))    # [(1,1), (2,2)]  -> el 3 se pierde

# zip con 3+ iterables
for a, b, c in zip([1,2], [3,4], [5,6]):
    print(a, b, c)
```

---

## 🔹 `while` — sintaxis básica

```python
contador = 0
while contador < 5:
    print(contador)
    contador += 1
```

```python
# while True + break -> patrón típico para loops controlados por lógica interna
while True:
    dato = input("Valor (q para salir): ")
    if dato == "q":
        break
    print(f"Procesando: {dato}")

# while con walrus operator (evita repetir código)
while (dato := input("Valor: ")) != "q":
    print(dato)
```

⚠️ **Gotcha:** cuidado con bucles `while` sin condición de salida clara → bucle infinito.

---

## 🔹 `break`, `continue`, `else` en bucles

| Palabra | Efecto |
|---|---|
| `break` | corta el bucle completamente |
| `continue` | salta a la siguiente iteración |
| `else` (en for/while) | se ejecuta si el bucle terminó SIN `break` |

```python
for valor in [1, 2, 3, 4, 5]:
    if valor == 3:
        continue         # salta el 3
    if valor == 5:
        break               # corta antes de imprimir el 5
    print(valor)
# 1, 2, 4

# else en bucle -> patrón poco conocido pero útil (ej: buscar un elemento)
for valor in [1, 2, 3]:
    if valor == 99:
        print("encontrado")
        break
else:
    print("no encontrado")     # se ejecuta porque no hubo break
```

---

## 🔹 Bucles anidados

```python
matriz = [[1, 2], [3, 4], [5, 6]]

for fila in matriz:
    for valor in fila:
        print(valor)

# break solo corta el bucle interno, no el externo
for i in range(3):
    for j in range(3):
        if j == 1:
            break
        print(i, j)
```

---

## 🔹 List / Dict / Set Comprehensions

### List comprehension

| Patrón | Sintaxis |
|---|---|
| Básica | `[expr for x in iterable]` |
| Con filtro | `[expr for x in iterable if cond]` |
| Con if/else | `[a if cond else b for x in iterable]` |
| Anidada (flatten) | `[x for fila in matriz for x in fila]` |

```python
cuadrados = [x**2 for x in range(6)]                # [0,1,4,9,16,25]
pares = [x for x in range(10) if x % 2 == 0]         # filtro
etiquetas = ["alto" if x > 50 else "bajo" for x in [30, 60, 45]]
```

### Dict comprehension

```python
cuadrados_dict = {x: x**2 for x in range(5)}
# {0:0, 1:1, 2:4, 3:9, 4:16}

nombres = ["a", "bb", "ccc"]
longitudes = {n: len(n) for n in nombres}
# {'a':1, 'bb':2, 'ccc':3}

# Invertir un diccionario
original = {"a": 1, "b": 2}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b'}
```

### Set comprehension

```python
unicos = {x % 3 for x in range(10)}     # {0, 1, 2}
```

### Generator expression (perezosa, no carga todo en memoria)

```python
gen = (x**2 for x in range(1000000))    # no calcula nada todavía
suma = sum(gen)                          # se calcula al recorrerlo
```

📌 Usa `()` en vez de `[]` cuando no necesitas la lista completa en memoria (datasets grandes).

---

## 🔹 Iterar sobre diccionarios

```python
sensores = {"T-101": 76.4, "T-102": 45.1}

for clave in sensores:                    # itera claves por defecto
    print(clave)

for clave, valor in sensores.items():      # claves + valores
    print(clave, valor)

for valor in sensores.values():             # solo valores
    print(valor)
```

---

## 🔹 `itertools` — combinaciones útiles (uso frecuente en Data Eng)

```python
from itertools import product, combinations, chain

list(product([1,2], ["a","b"]))       # [(1,'a'),(1,'b'),(2,'a'),(2,'b')]
list(combinations([1,2,3], 2))          # [(1,2),(1,3),(2,3)]
list(chain([1,2], [3,4]))                # [1,2,3,4] -> aplana iterables
```

---

## 🔹 Errores comunes

```python
# Modificar una lista mientras se itera sobre ella
l = [1, 2, 3, 4]
for x in l:
    if x == 2:
        l.remove(x)     # comportamiento inesperado, salta elementos
# Solución: iterar sobre copia o usar comprehension
l = [x for x in l if x != 2]

# Bucle infinito por olvidar actualizar la condición
i = 0
while i < 5:
    print(i)              # falta i += 1 -> bucle infinito

# range() no incluye el valor final
for i in range(5):
    pass                  # va de 0 a 4, NO incluye 5

# Confundir list comprehension con generator
suma = sum(x**2 for x in range(10))    # generator -> más eficiente en memoria
lista = [x**2 for x in range(10)]        # list -> ocupa memoria pero es reutilizable
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Iterar con índice | `for i, v in enumerate(lista):` |
| Iterar varias listas a la vez | `for a, b in zip(l1, l2):` |
| Rango de números | `for i in range(inicio, fin, paso):` |
| Cortar bucle | `break` |
| Saltar iteración | `continue` |
| Bucle hasta condición | `while cond:` |
| Crear lista filtrada/transformada | `[expr for x in it if cond]` |
| Crear diccionario | `{k: v for k, v in it}` |
| Generador (memoria eficiente) | `(expr for x in it)` |
| Combinaciones/productos | `itertools.product/combinations` |
