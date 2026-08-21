# 📘 Python Datasheet — Diccionarios (`dict`)

Colección de pares **clave-valor**, ordenada por inserción (desde Python 3.7+), mutable, claves únicas.

```python
sensor = {"nombre": "T-101", "tipo": "temperatura", "valor": 76.4}
```

---

## 🔹 Crear

```python
vacio       = {}
vacio       = dict()
directo     = {"a": 1, "b": 2}
con_dict    = dict(a=1, b=2)                     # solo con claves tipo string válidas
desde_pares = dict([("a", 1), ("b", 2)])            # desde lista de tuplas
desde_zip   = dict(zip(["a", "b"], [1, 2]))          # desde dos listas
comprehen   = {x: x**2 for x in range(5)}             # dict comprehension
fromkeys    = dict.fromkeys(["a", "b", "c"], 0)         # {'a':0,'b':0,'c':0}
```

---

## 🔹 Acceso a valores

| Código | Comportamiento |
|---|---|
| `d["clave"]` | error `KeyError` si no existe |
| `d.get("clave")` | devuelve `None` si no existe (no error) |
| `d.get("clave", default)` | devuelve `default` si no existe |
| `"clave" in d` | comprueba existencia → `bool` |

```python
d = {"nombre": "T-101", "valor": 76.4}

d["nombre"]                    # "T-101"
d["inexistente"]                # KeyError

d.get("inexistente")             # None
d.get("inexistente", "N/A")       # "N/A"

"nombre" in d                      # True  -> comprueba CLAVES
76.4 in d.values()                   # True  -> comprueba VALORES
```

---

## 🔹 Métodos que MODIFICAN

| Método | Qué hace | Ejemplo |
|---|---|---|
| `d[clave] = valor` | añade o sobrescribe | `d["nuevo"] = 1` |
| `.update(otro_dict)` | fusiona/sobrescribe con otro dict | `d.update({"a":1})` |
| `.setdefault(clave, default)` | devuelve valor; si no existe, lo crea con `default` | `d.setdefault("x", 0)` |
| `.pop(clave)` | elimina y devuelve el valor | `d.pop("a")` |
| `.pop(clave, default)` | igual, sin error si no existe | `d.pop("z", None)` |
| `.popitem()` | elimina y devuelve el último par (LIFO) | `d.popitem()` |
| `.clear()` | vacía el diccionario | `d.clear()` |
| `del d[clave]` | elimina la clave | `del d["a"]` |

```python
d = {"a": 1, "b": 2}

d["c"] = 3                     # {'a':1, 'b':2, 'c':3}
d.update({"a": 99, "d": 4})     # {'a':99, 'b':2, 'c':3, 'd':4}

valor = d.pop("b")               # valor=2, d={'a':99,'c':3,'d':4}
valor = d.pop("z", "no existe")    # no lanza error

# setdefault -> muy útil para inicializar contadores/listas sin comprobar antes
contador = {}
for letra in "abracadabra":
    contador.setdefault(letra, 0)
    contador[letra] += 1
# {'a':5, 'b':2, 'r':2, 'c':1, 'd':1}
```

---

## 🔹 Métodos de LECTURA / iteración

| Método | Devuelve |
|---|---|
| `.keys()` | vista de claves |
| `.values()` | vista de valores |
| `.items()` | vista de pares (clave, valor) |
| `.copy()` | copia superficial |
| `len(d)` | número de pares |

```python
d = {"nombre": "T-101", "tipo": "temperatura"}

for clave in d:                        # itera claves por defecto
    print(clave)

for clave, valor in d.items():           # claves + valores
    print(clave, valor)

list(d.keys())          # ['nombre', 'tipo']
list(d.values())          # ['T-101', 'temperatura']
list(d.items())            # [('nombre','T-101'), ('tipo','temperatura')]
```

---

## 🔹 Diccionarios anidados (muy común con JSON/APIs)

```python
sensores = {
    "T-101": {"tipo": "temperatura", "valor": 76.4, "activo": True},
    "T-102": {"tipo": "presion", "valor": 5.2, "activo": False}
}

sensores["T-101"]["valor"]                # 76.4
sensores["T-101"]["valor"] = 80.0           # modificar valor anidado

# Acceso seguro a anidados (evitar KeyError en cadena)
valor = sensores.get("T-999", {}).get("valor", "N/A")   # "N/A" sin error
```

---

## 🔹 Comprehensions con diccionarios

```python
precios = {"manzana": 1.5, "pera": 2.0, "uva": 3.5}

# Filtrar
caros = {k: v for k, v in precios.items() if v > 1.8}

# Transformar valores
con_iva = {k: round(v * 1.21, 2) for k, v in precios.items()}

# Invertir clave-valor
invertido = {v: k for k, v in precios.items()}

# Combinar dos listas en dict
claves = ["a", "b", "c"]
valores = [1, 2, 3]
combinado = {k: v for k, v in zip(claves, valores)}
```

---

## 🔹 Fusionar diccionarios

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}

# Método 1: unpacking (Python 3.5+)
fusion = {**d1, **d2}          # {'a':1, 'b':99, 'c':3}  -> d2 sobrescribe duplicados

# Método 2: operador | (Python 3.9+)
fusion = d1 | d2                 # mismo resultado, más legible

# Método 3: update (in-place, modifica d1)
d1.update(d2)
```

---

## 🔹 `collections` — utilidades muy usadas con diccionarios

```python
from collections import Counter, defaultdict

# Counter -> contar elementos automáticamente
palabras = ["a", "b", "a", "c", "a", "b"]
conteo = Counter(palabras)          # Counter({'a':3, 'b':2, 'c':1})
conteo.most_common(2)                 # [('a',3), ('b',2)]

# defaultdict -> evita comprobar si la clave existe
d = defaultdict(list)
d["sensores"].append("T-101")          # no hace falta inicializar la lista antes
d["sensores"].append("T-102")
print(d)                                 # defaultdict(<class 'list'>, {'sensores': ['T-101','T-102']})

d2 = defaultdict(int)                     # útil para contadores
d2["a"] += 1                                # arranca en 0 automáticamente
```

---

## 🔹 Ordenar diccionarios

```python
precios = {"pera": 2.0, "manzana": 1.5, "uva": 3.5}

# Por clave
dict(sorted(precios.items()))
# {'manzana': 1.5, 'pera': 2.0, 'uva': 3.5}

# Por valor
dict(sorted(precios.items(), key=lambda x: x[1]))
# {'manzana': 1.5, 'pera': 2.0, 'uva': 3.5}

# Por valor descendente
dict(sorted(precios.items(), key=lambda x: x[1], reverse=True))
```

---

## 🔹 Errores comunes

```python
d = {"a": 1}

d["b"]                      # KeyError: 'b'
d.get("b")                    # None -> forma segura

# Usar objeto mutable como clave
d[[1, 2]] = "valor"            # TypeError: unhashable type 'list'
d[(1, 2)] = "valor"              # ✅ las tuplas sí son válidas como clave

# Modificar dict mientras se itera sobre él
for clave in d:
    d[clave + "_nuevo"] = 1        # RuntimeError: dictionary changed size during iteration
# Solución: iterar sobre copia de claves
for clave in list(d.keys()):
    d[clave + "_nuevo"] = 1

# Confundir .keys() con lista (es una "vista", no una lista real)
claves = d.keys()
claves[0]                        # TypeError: no soporta indexado directo
claves_lista = list(d.keys())      # ✅ convertir primero
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Acceso seguro sin error | `d.get(clave, default)` |
| Añadir/actualizar | `d[clave] = valor` |
| Eliminar clave | `d.pop(clave)` / `del d[clave]` |
| Comprobar si existe clave | `clave in d` |
| Recorrer claves+valores | `for k, v in d.items():` |
| Fusionar dos dicts | `d1 \| d2` |
| Contar elementos | `Counter(lista)` |
| Inicializar sin comprobar | `defaultdict(list)` |
| Invertir clave-valor | `{v: k for k, v in d.items()}` |
| Ordenar por valor | `sorted(d.items(), key=lambda x: x[1])` |
| Acceso seguro anidado | `d.get("a", {}).get("b", "N/A")` |
