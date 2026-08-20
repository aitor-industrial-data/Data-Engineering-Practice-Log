# 📘 Python Datasheet — Operadores

---

## 🔹 Aritméticos

| Operador | Operación | Ejemplo | Resultado |
|---|---|---|---|
| `+` | Suma | `5 + 2` | `7` |
| `-` | Resta | `5 - 2` | `3` |
| `*` | Multiplicación | `5 * 2` | `10` |
| `/` | División (float siempre) | `5 / 2` | `2.5` |
| `//` | División entera (floor) | `5 // 2` | `2` |
| `%` | Módulo (resto) | `5 % 2` | `1` |
| `**` | Potencia | `5 ** 2` | `25` |

```python
5 / 2      # 2.5   -> siempre devuelve float
5 // 2     # 2     -> trunca hacia abajo
-5 // 2    # -3    -> ojo: redondea hacia -infinito, no hacia 0
5 % 2      # 1
2 ** 0.5   # 1.4142135623730951  -> raíz cuadrada
```

⚠️ **Gotcha:** `//` con negativos no simplemente "trunca", redondea hacia abajo (-infinito):
```python
7 // 2      # 3
-7 // 2     # -4  (no -3)
```

---

## 🔹 Comparación (devuelven `bool`)

| Operador | Significado | Ejemplo |
|---|---|---|
| `==` | Igual (valor) | `5 == 5` → `True` |
| `!=` | Distinto | `5 != 3` → `True` |
| `>` | Mayor que | `5 > 3` → `True` |
| `<` | Menor que | `5 < 3` → `False` |
| `>=` | Mayor o igual | `5 >= 5` → `True` |
| `<=` | Menor o igual | `5 <= 4` → `False` |

```python
# Encadenamiento (muy Python, poco común en otros lenguajes)
x = 5
0 < x < 10          # True  -> equivale a (0 < x) and (x < 10)
temp = 76.4
20 <= temp <= 100    # rango de validez en una sola línea
```

---

## 🔹 Lógicos

| Operador | Significado | Ejemplo |
|---|---|---|
| `and` | Y (ambas True) | `True and False` → `False` |
| `or` | O (al menos una True) | `True or False` → `True` |
| `not` | Negación | `not True` → `False` |

```python
temp = 90
activo = True
if temp > 80 and activo:
    print("Alarma activa")

# Evaluación "corto-circuito" (short-circuit)
# Python NO devuelve solo True/False con and/or: devuelve el operando
0 or "por defecto"     # "por defecto"  (0 es falsy, sigue evaluando)
5 or "por defecto"      # 5              (5 es truthy, se queda ahí)
5 and "siguiente"        # "siguiente"   (5 es truthy, sigue)
0 and "siguiente"         # 0             (0 es falsy, corta ahí)
```

📌 Este comportamiento es la base de patrones como `valor = entrada or "default"` (valor por defecto si `entrada` es falsy).

---

## 🔹 Asignación (compuestos)

| Operador | Equivale a | Ejemplo |
|---|---|---|
| `=` | asignación simple | `x = 5` |
| `+=` | `x = x + n` | `x += 1` |
| `-=` | `x = x - n` | `x -= 1` |
| `*=` | `x = x * n` | `x *= 2` |
| `/=` | `x = x / n` | `x /= 2` |
| `//=` | `x = x // n` | `x //= 2` |
| `%=` | `x = x % n` | `x %= 2` |
| `**=` | `x = x ** n` | `x **= 2` |

```python
contador = 0
contador += 1     # 1
contador **= 3     # 1
total = 100
total -= 25         # 75
```

---

## 🔹 Identidad (`is` / `is not`)

Compara si dos variables apuntan al **mismo objeto en memoria** (no si tienen el mismo valor).

```python
a = [1, 2]
b = [1, 2]
a == b        # True  (mismo contenido)
a is b        # False (objetos distintos)

x = None
x is None       # True  <- forma correcta, NUNCA uses x == None
x is not None   # True si tiene valor
```

---

## 🔹 Pertenencia (`in` / `not in`)

Funciona sobre listas, tuplas, sets, dicts (claves) y strings.

```python
lista = [1, 2, 3]
2 in lista            # True
5 not in lista         # True

texto = "python"
"th" in texto           # True (substring)

diccionario = {"a": 1, "b": 2}
"a" in diccionario       # True -> comprueba claves, no valores
1 in diccionario.values()  # True -> así sí comprueba valores
```

---

## 🔹 Bit a bit (bitwise) — uso ocasional

| Operador | Significado | Ejemplo |
|---|---|---|
| `&` | AND bit a bit | `5 & 3` → `1` |
| `\|` | OR bit a bit | `5 \| 3` → `7` |
| `^` | XOR | `5 ^ 3` → `6` |
| `~` | NOT (complemento) | `~5` → `-6` |
| `<<` | Desplaza izquierda | `5 << 1` → `10` |
| `>>` | Desplaza derecha | `5 >> 1` → `2` |

```python
# Uso típico: flags/permisos, o trucos de rendimiento
5 << 1     # 10  -> equivale a multiplicar por 2
5 >> 1     # 2   -> equivale a dividir entre 2 (entero)
```

---

## 🔹 Precedencia (orden de evaluación) — de mayor a menor

| Prioridad | Operadores |
|---|---|
| 1 (máxima) | `()` paréntesis |
| 2 | `**` potencia |
| 3 | `*`, `/`, `//`, `%` |
| 4 | `+`, `-` |
| 5 | comparaciones `==`, `!=`, `<`, `>`, etc. |
| 6 | `not` |
| 7 | `and` |
| 8 (mínima) | `or` |

```python
2 + 3 * 4          # 14, no 20 (* antes que +)
(2 + 3) * 4         # 20 -> paréntesis fuerza el orden
not True or True     # True  -> not se aplica primero: (not True) or True
```

📌 **Regla práctica:** si dudas del orden, mete paréntesis. Es más legible y evita errores.

---

## 🔹 Errores comunes

```python
# Confundir = con ==
if x = 5:            # SyntaxError
if x == 5:            # ✅

# Usar == con None en vez de is
if x == None:          # funciona pero NO es la forma recomendada
if x is None:            # ✅ forma pythonica

# División entre 0
10 / 0                  # ZeroDivisionError
10 // 0                 # ZeroDivisionError

# Olvidar que / siempre da float
resultado = 10 / 2       # 5.0, no 5 (int)
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| División exacta con decimales | `a / b` |
| División entera | `a // b` |
| Resto | `a % b` |
| Potencia / raíz | `a ** b` / `a ** 0.5` |
| Comprobar rango | `0 < x < 100` |
| Valor por defecto si falsy | `valor = entrada or "default"` |
| Comprobar None | `x is None` |
| Comprobar pertenencia | `x in coleccion` |
| Negar condición | `not condicion` |
