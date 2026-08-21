# 📘 Python Datasheet — Tuplas (`tuple`)

Colección **ordenada, inmutable, permite duplicados**. Como una lista pero no se puede modificar tras crearla.

```python
tupla = (10, 20, 30, "texto", True)
```

---

## 🔹 Crear

```python
vacia        = ()
vacia        = tuple()
directa      = (1, 2, 3)
sin_parentesis = 1, 2, 3          # también es tupla (por las comas)
un_elemento  = (5,)               # ⚠️ la coma es OBLIGATORIA, si no es un int
no_es_tupla  = (5)                # esto es solo un int entre paréntesis
desde_lista  = tuple([1, 2, 3])
desde_str    = tuple("abc")        # ('a', 'b', 'c')
```

---

## 🔹 Acceso e indexado (igual que listas)

```python
t = (10, 20, 30, 40, 50)
t[0]        # 10
t[-1]        # 50
t[1:4]        # (20, 30, 40)
t[::-1]        # (50, 40, 30, 20, 10)
```

---

## 🔹 Por qué usar tuplas en vez de listas

| Ventaja | Explicación |
|---|---|
| Inmutabilidad | garantiza que los datos no cambian por accidente |
| Más rápidas | menor overhead que listas (uso de memoria y velocidad) |
| Hashable | se pueden usar como claves de diccionario o en sets |
| Semántica | comunica "esto es un registro fijo", no una colección editable |

```python
# Las tuplas SÍ se pueden usar como clave de dict, las listas NO
coordenadas = {(0, 0): "origen", (1, 1): "diagonal"}

# lista como clave -> error
# {[0, 0]: "origen"}    # TypeError: unhashable type: 'list'
```

---

## 🔹 Métodos disponibles (muy pocos, por ser inmutable)

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.count(x)` | cuenta ocurrencias | `t.count(20)` |
| `.index(x)` | índice de la primera ocurrencia | `t.index(30)` |

```python
t = (1, 2, 2, 3, 2)
t.count(2)     # 3
t.index(3)      # 3
```

📌 No existen `.append()`, `.remove()`, `.sort()`, etc. — para eso hay que convertir a lista, modificar y volver a tupla si hace falta.

```python
t = (3, 1, 2)
lista_temp = list(t)
lista_temp.sort()
t_ordenada = tuple(lista_temp)     # (1, 2, 3)
```

---

## 🔹 Desempaquetado (packing / unpacking) — su uso más común

```python
sensor = ("T-101", "temperatura", 76.4)
nombre, tipo, valor = sensor          # desempaquetado directo

# Desempaquetado extendido
primero, *resto = (1, 2, 3, 4)
print(primero, resto)                  # 1 [2, 3, 4]

*inicio, ultimo = (1, 2, 3, 4)
print(inicio, ultimo)                   # [1, 2, 3] 4

# Ignorar valores con _
nombre, _, valor = ("T-101", "temperatura", 76.4)
```

---

## 🔹 Funciones que devuelven múltiples valores (usan tuplas internamente)

```python
def estadisticas(valores):
    return min(valores), max(valores), sum(valores)/len(valores)   # devuelve tupla

minimo, maximo, media = estadisticas([10, 20, 30])
print(minimo, maximo, media)     # 10 30 20.0
```

---

## 🔹 Namedtuple (tupla con nombres de campo — muy usado en Data Eng)

```python
from collections import namedtuple

Sensor = namedtuple("Sensor", ["nombre", "tipo", "valor"])
s = Sensor("T-101", "temperatura", 76.4)

s.nombre       # 'T-101'   -> acceso por nombre, más legible que s[0]
s.valor         # 76.4
s[0]             # 'T-101'   -> también funciona por índice

# Convertir a diccionario
s._asdict()       # {'nombre': 'T-101', 'tipo': 'temperatura', 'valor': 76.4}
```

📌 Ideal para representar registros/filas (como una fila de CSV o de un DataFrame) sin necesidad de crear una clase completa.

---

## 🔹 Concatenar y repetir

```python
a = (1, 2)
b = (3, 4)
c = a + b        # (1, 2, 3, 4) -> crea tupla nueva
d = a * 3          # (1, 2, 1, 2, 1, 2)
```

---

## 🔹 Comparación con listas

| Característica | Lista | Tupla |
|---|---|---|
| Mutable | Sí | No |
| Sintaxis | `[1, 2, 3]` | `(1, 2, 3)` |
| Métodos disponibles | Muchos | Pocos (`count`, `index`) |
| Como clave de dict | ❌ No | ✅ Sí |
| Rendimiento | Más lenta | Más rápida |
| Uso típico | Colección que cambia | Registro fijo / retorno múltiple |

---

## 🔹 Errores comunes

```python
t = (1, 2, 3)
t[0] = 99                     # TypeError: 'tuple' object does not support item assignment

t.append(4)                    # AttributeError: no existe .append en tuplas

x = (5)                         # ⚠️ esto es int, no tupla (falta la coma)
x = (5,)                          # ✅ esto SÍ es tupla

# Tupla "inmutable" con contenido mutable dentro -> ¡puede sorprender!
t = ([1, 2], [3, 4])
t[0].append(99)                    # ✅ funciona: la lista interna SÍ es mutable
print(t)                            # ([1, 2, 99], [3, 4])
# La tupla es inmutable en su ESTRUCTURA (no puedes reasignar t[0]),
# pero si contiene objetos mutables, esos sí pueden cambiar por dentro.
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Crear tupla | `(1, 2, 3)` |
| Tupla de 1 elemento | `(5,)` (con coma) |
| Desempaquetar | `a, b, c = tupla` |
| Ignorar valor al desempaquetar | `a, _, c = tupla` |
| Contar ocurrencias | `t.count(x)` |
| Buscar índice | `t.index(x)` |
| Convertir a lista y volver | `tuple(list(t))` |
| Tupla con nombres de campo | `namedtuple("Nombre", ["campo1","campo2"])` |
| Usar como clave de dict | `{(0,0): "valor"}` |
