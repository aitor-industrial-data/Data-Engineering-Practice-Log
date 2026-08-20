# 📘 Python Datasheet — Variables y Tipos de Datos

No se declara el tipo: lo determina el valor asignado (tipado dinámico).

```python
x = 10
x = "ahora soy texto"   # válido, x cambia de tipo
```

---

## 🔹 Tipos nativos

| Tipo | Ejemplo | Mutable | `type()` |
|---|---|---|---|
| Entero | `42` | No | `int` |
| Decimal | `3.14` | No | `float` |
| Complejo | `2+3j` | No | `complex` |
| Texto | `"hola"` | No | `str` |
| Booleano | `True` / `False` | No | `bool` |
| Lista | `[1, 2, 3]` | **Sí** | `list` |
| Tupla | `(1, 2, 3)` | No | `tuple` |
| Diccionario | `{"a": 1}` | **Sí** | `dict` |
| Set | `{1, 2, 3}` | **Sí** | `set` |
| Nulo | `None` | — | `NoneType` |

```python
type(42)                    # <class 'int'>
isinstance(42, int)         # True  <- preferir sobre type()
```

---

## 🔹 Naming (reglas rápidas)

| Regla | ✅ Válido | ❌ Inválido |
|---|---|---|
| Empieza por letra o `_` | `_temp`, `temp1` | `1temp` |
| Sin espacios | `nombre_sensor` | `nombre sensor` |
| Case sensitive | `valor` ≠ `Valor` | — |
| No palabra reservada | `clase_activo` | `class` |
| Convención (PEP8) | `snake_case` | `CamelCase` (eso es para clases) |

```python
import keyword
keyword.kwlist       # lista completa de palabras reservadas
```

---

## 🔹 Asignación

| Patrón | Código |
|---|---|
| Simple | `x = 10` |
| Múltiple (valores distintos) | `a, b, c = 1, 2, 3` |
| Múltiple (mismo valor) | `a = b = c = 0` |
| Desempaquetar lista/tupla | `x, y = [10, 20]` |
| Desempaquetado extendido | `primero, *resto = [1,2,3,4]` |
| Aumentada | `x += 1` / `x *= 2` / `x -= 3` |
| Intercambiar valores | `a, b = b, a` |

```python
primero, *resto = [10, 20, 30, 40]
print(primero, resto)   # 10 [20, 30, 40]
```

---

## 🔹 Conversión de tipos (casting)

| Función | Convierte a | Ejemplo | Resultado |
|---|---|---|---|
| `int(x)` | entero | `int("45")` | `45` |
| `int(x)` | entero desde float | `int(4.9)` | `4` (trunca) |
| `float(x)` | decimal | `float("3.8")` | `3.8` |
| `str(x)` | texto | `str(120)` | `"120"` |
| `bool(x)` | booleano | `bool(0)` | `False` |
| `list(x)` | lista | `list("abc")` | `['a','b','c']` |

```python
# str con decimal no se convierte directo a int -> error
int("48.7")              # ValueError
int(float("48.7"))       # 48  <- forma correcta
```

---

## 🔹 Valores "falsy" (se evalúan como `False`)

```python
0, 0.0, "", [], {}, (), set(), None, False
```
Todo lo demás es `True`. Por eso `if lista:` es más pythonico que `if len(lista) > 0:`.

---

## 🔹 `==` vs `is`

| Operador | Compara | Usar para |
|---|---|---|
| `==` | **valor** | comparar contenido: números, strings, listas... |
| `is` | **identidad** (mismo objeto en memoria) | `is None`, `is True` |

```python
a = [1, 2]
b = [1, 2]
a == b     # True  (mismo contenido)
a is b     # False (objetos distintos en memoria)

x = None
x is None  # True <- forma correcta de comprobar None
```

---

## 🔹 Constantes

Python no tiene `const` real. Por convención, MAYÚSCULAS = "no tocar":

```python
LIMITE_TEMP_MAX = 85.0
FACTOR_CONVERSION_KW = 1.36
```

---

## 🔹 Copiar vs referenciar (mutables)

```python
original = [1, 2, 3]
copia = original            # ⚠️ NO copia, apunta al MISMO objeto
copia.append(4)
print(original)             # [1, 2, 3, 4]  <- cambió también

copia_real = original.copy()   # o list(original) o original[:]
```

---

## 🔹 Errores comunes

```python
print(no_existe)                    # NameError: no definida

"Edad: " + 30                        # TypeError: str + int
"Edad: " + str(30)                   # ✅ correcto

if temperatura = 30:                 # SyntaxError (falta ==)
if temperatura == 30:                # ✅ correcto

lista = [1, 2, 3]
copia = lista                        # comparten memoria (ver arriba)
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Ver tipo | `type(x)` / `isinstance(x, int)` |
| Convertir a int/float/str | `int(x)` / `float(x)` / `str(x)` |
| Comprobar si es None | `x is None` |
| Comparar contenido | `a == b` |
| Comparar identidad | `a is b` |
| Copiar lista (nivel 1) | `l.copy()` / `l[:]` |
| Intercambiar variables | `a, b = b, a` |
| Ver palabras reservadas | `keyword.kwlist` |
| Constante (convención) | `NOMBRE = valor` (mayúsculas) |
