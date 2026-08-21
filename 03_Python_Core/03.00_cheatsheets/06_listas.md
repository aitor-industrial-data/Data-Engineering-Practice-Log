# 📘 Python Datasheet — Listas (`list`)

Colección **ordenada, mutable, permite duplicados**. Índices desde `0`.

```python
lista = [10, 20, 30, "texto", True]
```

---

## 🔹 Crear

```python
vacia      = []
vacia      = list()
directa    = [1, 2, 3]
por_rango  = list(range(5))          # [0, 1, 2, 3, 4]
repetida   = [0] * 5                 # [0, 0, 0, 0, 0]
desde_str  = list("abc")             # ['a', 'b', 'c']
comprehen  = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```

---

## 🔹 Acceso e indexado

| Código | Resultado |
|---|---|
| `lista[0]` | primer elemento |
| `lista[-1]` | último elemento |
| `lista[2:5]` | slice índices 2,3,4 |
| `lista[:3]` | del inicio hasta índice 2 |
| `lista[3:]` | de índice 3 hasta el final |
| `lista[::2]` | de 2 en 2 |
| `lista[::-1]` | lista invertida |
| `lista[-3:]` | últimos 3 elementos |

```python
datos = [10, 20, 30, 40, 50]
print(datos[1:4])    # [20, 30, 40]
print(datos[::-1])   # [50, 40, 30, 20, 10]
```

---

## 🔹 Métodos que MODIFICAN la lista (in-place, devuelven `None`)

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.append(x)` | añade al final | `l.append(6)` |
| `.insert(i, x)` | inserta en posición `i` | `l.insert(0, 99)` |
| `.extend(iterable)` | añade varios elementos | `l.extend([7,8])` |
| `.remove(x)` | elimina primera ocurrencia de valor `x` | `l.remove(20)` |
| `.pop(i)` | elimina y devuelve elemento en índice `i` (o último si vacío) | `l.pop()` |
| `.clear()` | vacía la lista | `l.clear()` |
| `.sort()` | ordena in-place (asc por defecto) | `l.sort(reverse=True)` |
| `.reverse()` | invierte in-place | `l.reverse()` |

```python
l = [3, 1, 4, 1, 5]
l.append(9)          # [3, 1, 4, 1, 5, 9]
l.remove(1)           # [3, 4, 1, 5, 9]  <- solo el PRIMER 1
l.sort()               # [1, 3, 4, 5, 9]
l.sort(reverse=True)   # [9, 5, 4, 3, 1]
ultimo = l.pop()        # ultimo=1, l=[9,5,4,3]
```

⚠️ **Gotcha:** `.sort()` devuelve `None`, no la lista. Este error es muy típico:
```python
l = l.sort()   # MAL -> l ahora es None
```

---

## 🔹 Métodos que NO modifican (devuelven algo nuevo)

| Método/función | Qué hace | Ejemplo |
|---|---|---|
| `.copy()` | copia superficial | `l2 = l.copy()` |
| `sorted(l)` | devuelve nueva lista ordenada | `sorted(l, reverse=True)` |
| `.index(x)` | devuelve índice de la primera ocurrencia | `l.index(4)` |
| `.count(x)` | cuenta ocurrencias de `x` | `l.count(1)` |
| `len(l)` | número de elementos | `len(l)` |
| `sum(l)` | suma (numéricos) | `sum(l)` |
| `max(l)` / `min(l)` | máximo / mínimo | `max(l)` |
| `x in l` | comprueba pertenencia → bool | `4 in l` |

```python
l = [4, 1, 4, 2, 4]
print(l.count(4))     # 3
print(l.index(4))     # 0 (primera aparición)
print(sorted(l))       # [1, 2, 4, 4, 4] -> l NO cambia
print(4 in l)          # True
```

---

## 🔹 Unir lista en un string — `.join()`

⚠️ `.join()` es un método de **string**, no de lista — se llama sobre el separador, no sobre la lista. Se pone aquí porque es la forma más habitual de "convertir una lista en texto".

```python
lista = ["T-101", "temperatura", "76.4"]

",".join(lista)          # "T-101,temperatura,76.4"
" ".join(lista)            # "T-101 temperatura 76.4"
"".join(lista)               # "T-101temperatura76.4"  (sin separador)
"\n".join(lista)               # una por línea
```

Todos los elementos deben ser `str`, si no da error:
```python
numeros = [1, 2, 3]
",".join(numeros)                    # ❌ TypeError: expected str instance, int found
",".join(map(str, numeros))            # ✅ "1,2,3"
",".join(str(n) for n in numeros)        # ✅ "1,2,3"  (con generator, igual de válido)
```

📌 Es la forma recomendada de concatenar muchos elementos, mucho más eficiente que hacer `+=` dentro de un bucle.

---

## 🔹 Concatenar / repetir

```python
a = [1, 2]
b = [3, 4]
c = a + b            # [1, 2, 3, 4]  -> crea lista nueva
a += b                # equivalente a a.extend(b), modifica in-place
d = a * 3             # repite la lista 3 veces
```

---

## 🔹 Copia superficial vs profunda (clave con listas anidadas)

```python
import copy

original = [[1, 2], [3, 4]]

superficial = original.copy()        # o list(original) o original[:]
superficial[0].append(99)
print(original)   # [[1, 2, 99], [3, 4]]  <- ¡también cambió!

profunda = copy.deepcopy(original)
profunda[0].append(100)
print(original)   # NO cambia
```

📌 `.copy()` / `list(x)` / `x[:]` → copia solo el primer nivel. Si hay listas dentro de listas, comparten referencia. Usa `copy.deepcopy()` para anidados.

---

## 🔹 List Comprehensions (imprescindible)

```python
cuadrados   = [x**2 for x in range(6)]                    # [0,1,4,9,16,25]
pares       = [x for x in range(10) if x % 2 == 0]        # filtro
transformada = [x*2 if x > 5 else x for x in range(10)]    # if/else inline
aplanada    = [x for fila in [[1,2],[3,4]] for x in fila]  # [1,2,3,4]
```

| Patrón | Sintaxis |
|---|---|
| Básica | `[expr for x in iterable]` |
| Con filtro | `[expr for x in iterable if condicion]` |
| Con if/else | `[expr_si if cond else expr_no for x in iterable]` |
| Anidada (flatten) | `[x for sub in lista for x in sub]` |

---

## 🔹 Recorrer listas

```python
datos = [230, 231, 229]

for valor in datos:
    print(valor)

for i, valor in enumerate(datos):        # con índice
    print(i, valor)

for v1, v2 in zip(datos, [1, 2, 3]):     # dos listas a la vez
    print(v1, v2)
```

---

## 🔹 Ordenar con clave personalizada (`key=`)

```python
sensores = [("T-101", 76.4), ("T-102", 45.1), ("T-103", 90.0)]

# Ordenar por temperatura (segundo elemento de la tupla)
por_temp = sorted(sensores, key=lambda x: x[1])
# [('T-102', 45.1), ('T-101', 76.4), ('T-103', 90.0)]

por_temp_desc = sorted(sensores, key=lambda x: x[1], reverse=True)

# Con múltiples criterios
datos = [{"nombre": "A", "prioridad": 2}, {"nombre": "B", "prioridad": 1}]
ordenado = sorted(datos, key=lambda d: d["prioridad"])
```

---

## 🔹 Listas + funciones útiles

```python
l = [1, 2, 3, 4, 5]

any(x > 4 for x in l)      # True  -> ¿algún elemento cumple?
all(x > 0 for x in l)      # True  -> ¿TODOS cumplen?
list(map(lambda x: x*2, l))     # [2,4,6,8,10]
list(filter(lambda x: x%2==0, l))  # [2, 4]
from functools import reduce
reduce(lambda a,b: a+b, l)   # 15 (suma acumulada)
```

---

## 🔹 Errores comunes

```python
l = [1, 2, 3]

l[5]                # IndexError: list index out of range
l.remove(99)         # ValueError: 99 no está en la lista

# Modificar una lista mientras la recorres -> comportamiento inesperado
for x in l:
    if x == 2:
        l.remove(x)   # MAL: salta elementos al desplazarse los índices
# Solución: iterar sobre copia
for x in l.copy():
    if x == 2:
        l.remove(x)

# o mejor: comprehension
l = [x for x in l if x != 2]
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Añadir al final | `l.append(x)` |
| Insertar en posición | `l.insert(i, x)` |
| Quitar por valor | `l.remove(x)` |
| Quitar por índice | `l.pop(i)` / `del l[i]` |
| Vaciar | `l.clear()` |
| Ordenar (in-place) | `l.sort()` |
| Ordenar (nueva lista) | `sorted(l)` |
| Invertir | `l.reverse()` / `l[::-1]` |
| Copiar (nivel 1) | `l.copy()` / `l[:]` |
| Copiar (anidada) | `copy.deepcopy(l)` |
| Buscar índice | `l.index(x)` |
| Contar ocurrencias | `l.count(x)` |
| Comprobar si existe | `x in l` |
| Longitud | `len(l)` |
| Filtrar+transformar | `[f(x) for x in l if cond]` |
| Convertir lista a string | `",".join(l)` (elementos deben ser str) |
