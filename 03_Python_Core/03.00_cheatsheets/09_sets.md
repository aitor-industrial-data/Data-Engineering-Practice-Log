# 📘 Python Datasheet — Sets (`set`)

Colección **no ordenada, mutable, sin duplicados**. Ideal para comprobar pertenencia rápido y operaciones de conjuntos (unión, intersección...).

```python
sensores_activos = {"T-101", "T-102", "T-103"}
```

---

## 🔹 Crear

```python
vacio       = set()              # ⚠️ {} crea un DICCIONARIO vacío, no un set
directo     = {1, 2, 3}
desde_lista = set([1, 2, 2, 3])    # {1, 2, 3} -> elimina duplicados automáticamente
desde_str   = set("aabbcc")          # {'a', 'b', 'c'}
comprehen   = {x % 3 for x in range(10)}    # set comprehension
frozen      = frozenset([1, 2, 3])            # versión INMUTABLE de un set
```

⚠️ **Gotcha:** `{}` NO crea un set vacío, crea un diccionario vacío. Usa siempre `set()`.

---

## 🔹 Uso principal: eliminar duplicados

```python
lista_con_duplicados = [1, 2, 2, 3, 3, 3, 4]
unicos = list(set(lista_con_duplicados))     # [1, 2, 3, 4] (orden no garantizado)

# Contar valores únicos rápidamente
lecturas = ["T-101", "T-102", "T-101", "T-103", "T-101"]
sensores_distintos = len(set(lecturas))         # 3
```

---

## 🔹 Métodos que MODIFICAN

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.add(x)` | añade un elemento | `s.add(4)` |
| `.update(iterable)` | añade varios elementos | `s.update([4,5])` |
| `.remove(x)` | elimina `x`, error si no existe | `s.remove(2)` |
| `.discard(x)` | elimina `x`, sin error si no existe | `s.discard(99)` |
| `.pop()` | elimina y devuelve un elemento arbitrario | `s.pop()` |
| `.clear()` | vacía el set | `s.clear()` |

```python
s = {1, 2, 3}
s.add(4)                # {1,2,3,4}
s.update([5, 6])          # {1,2,3,4,5,6}
s.remove(1)                 # {2,3,4,5,6}
s.discard(99)                 # no da error aunque 99 no exista
s.remove(99)                    # ❌ KeyError: 99 no existe
```

---

## 🔹 Operaciones de conjuntos (lo más potente de los sets)

| Operación | Operador | Método | Resultado |
|---|---|---|---|
| Unión | `\|` | `.union()` | elementos de ambos |
| Intersección | `&` | `.intersection()` | elementos comunes |
| Diferencia | `-` | `.difference()` | en A pero no en B |
| Diferencia simétrica | `^` | `.symmetric_difference()` | en A o B, no en ambos |
| Subconjunto | `<=` | `.issubset()` | A está contenido en B |
| Superconjunto | `>=` | `.issuperset()` | A contiene a B |
| Disjuntos | — | `.isdisjoint()` | no comparten elementos |

```python
sensores_planta_a = {"T-101", "T-102", "T-103"}
sensores_alarma    = {"T-102", "T-105"}

sensores_planta_a | sensores_alarma      # {'T-101','T-102','T-103','T-105'} -> unión
sensores_planta_a & sensores_alarma      # {'T-102'}  -> intersección (en ambos)
sensores_planta_a - sensores_alarma      # {'T-101','T-103'}  -> solo en planta_a
sensores_planta_a ^ sensores_alarma      # {'T-101','T-103','T-105'}  -> exclusivos de cada uno

{"T-101"}.issubset(sensores_planta_a)      # True
sensores_planta_a.issuperset({"T-101"})      # True
```

📌 **Caso de uso típico en Data Eng:** comparar dos conjuntos de IDs (ej: qué registros están en un dataset pero no en otro).

```python
ids_dataset_1 = {"A1", "A2", "A3", "A4"}
ids_dataset_2 = {"A3", "A4", "A5"}

solo_en_1 = ids_dataset_1 - ids_dataset_2     # {'A1', 'A2'}
comunes    = ids_dataset_1 & ids_dataset_2      # {'A3', 'A4'}
```

---

## 🔹 Pertenencia (muy rápida, O(1) en promedio)

```python
sensores_activos = {"T-101", "T-102", "T-103"}

"T-101" in sensores_activos           # True -> mucho más rápido que "in lista" con datasets grandes
```

📌 **Por qué importa:** comprobar `x in lista` es O(n) (recorre todo), pero `x in set` es O(1) aproximadamente. Con datasets grandes, usar sets para comprobaciones de pertenencia es una optimización clave.

---

## 🔹 Recorrer un set

```python
for sensor in {"T-101", "T-102", "T-103"}:
    print(sensor)          # orden no garantizado (aunque en la práctica suele mantenerse por inserción)
```

---

## 🔹 `frozenset` — versión inmutable

```python
fs = frozenset([1, 2, 3])
fs.add(4)                     # AttributeError: no se puede modificar

# Útil como clave de diccionario o elemento de otro set (los sets normales no son hashables)
d = {frozenset([1,2]): "grupo A"}
```

---

## 🔹 Errores comunes

```python
vacio = {}                    # ❌ esto es un DICT vacío, no un set
vacio = set()                   # ✅ set vacío correcto

s = {1, 2, 3}
s[0]                             # TypeError: los sets no soportan indexado (no hay orden garantizado)

s.remove(99)                       # KeyError si el elemento no existe
s.discard(99)                        # ✅ forma segura, no da error

# Los sets no admiten elementos mutables (listas, dicts) dentro
s.add([1, 2])                          # TypeError: unhashable type: 'list'
s.add((1, 2))                            # ✅ las tuplas sí son válidas
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Crear set vacío | `set()` (nunca `{}`) |
| Eliminar duplicados de lista | `list(set(lista))` |
| Añadir elemento | `s.add(x)` |
| Eliminar sin error | `s.discard(x)` |
| Comprobar pertenencia (rápido) | `x in s` |
| Elementos comunes | `a & b` |
| Elementos de ambos | `a \| b` |
| Solo en A | `a - b` |
| Solo en uno de los dos | `a ^ b` |
| ¿A contenido en B? | `a <= b` / `a.issubset(b)` |
| Versión inmutable | `frozenset(iterable)` |
