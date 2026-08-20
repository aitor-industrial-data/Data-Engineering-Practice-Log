# 📘 Python Datasheet — Estructuras de Control (if / elif / else)

---

## 🔹 Sintaxis básica

```python
if condicion:
    # bloque si se cumple
elif otra_condicion:
    # bloque si se cumple la segunda
else:
    # bloque si ninguna se cumple
```

📌 Python usa **indentación** (4 espacios, no tabs) para delimitar bloques, no llaves `{}`.

```python
temp = 76.4

if temp >= 90:
    print("Crítico")
elif temp >= 70:
    print("Alerta")
else:
    print("Normal")
# Alerta
```

---

## 🔹 Condicional simple (una línea)

```python
if temp > 80: print("alerta")     # válido pero poco recomendado (poca legibilidad)

# Operador ternario (condicional en una línea) -> MUY usado
estado = "alerta" if temp > 80 else "normal"
```

| Patrón | Sintaxis |
|---|---|
| Ternario básico | `x if cond else y` |
| Ternario anidado | `x if c1 else (y if c2 else z)` |
| Asignación por defecto | `valor = entrada or "default"` |

```python
nivel = "alto" if temp > 80 else "medio" if temp > 50 else "bajo"
```

---

## 🔹 Anidamiento

```python
temp = 76.4
activo = True

if activo:
    if temp > 90:
        print("Crítico y activo")
    else:
        print("Activo, sin alarma")
else:
    print("Inactivo")
```

📌 **Mejor práctica:** evitar anidar más de 2-3 niveles. Se puede aplanar con `and`:

```python
# En vez de anidar...
if activo:
    if temp > 90:
        print("Crítico")

# ...combinar condiciones
if activo and temp > 90:
    print("Crítico")
```

---

## 🔹 Condiciones múltiples

```python
temp = 76.4
presion = 5.2

if temp > 80 and presion > 5:
    print("doble alarma")

if temp > 80 or presion > 10:
    print("al menos una alarma")

if not (temp > 80):
    print("temperatura OK")
```

---

## 🔹 Comprobación de tipos "truthy"/"falsy" (muy pythonico)

```python
lista = []
# En vez de:
if len(lista) == 0:
    print("vacía")
# Mejor:
if not lista:
    print("vacía")

nombre = ""
if not nombre:
    print("sin nombre")

valor = None
if valor is None:            # forma correcta para None
    print("sin valor")
```

| Falsy | Truthy |
|---|---|
| `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`, `None`, `False` | cualquier otro valor |

---

## 🔹 `match` / `case` (Python ≥ 3.10, equivalente a switch)

```python
codigo_error = 404

match codigo_error:
    case 200:
        print("OK")
    case 404:
        print("No encontrado")
    case 500 | 502 | 503:          # varios valores con |
        print("Error de servidor")
    case _:                          # caso por defecto (equivalente a else)
        print("Código desconocido")
```

```python
# match también permite desestructurar estructuras (pattern matching)
punto = (0, 5)
match punto:
    case (0, 0):
        print("origen")
    case (0, y):
        print(f"eje Y en {y}")
    case (x, 0):
        print(f"eje X en {x}")
    case (x, y):
        print(f"punto en ({x}, {y})")
```

---

## 🔹 `pass`, `break`, `continue` dentro de condicionales

```python
if temp > 80:
    pass          # no hace nada -> útil como placeholder mientras desarrollas

for valor in [1, 2, 3, 4, 5]:
    if valor == 3:
        continue    # salta esta iteración, sigue con la siguiente
    if valor == 5:
        break         # corta el bucle por completo
    print(valor)
# 1, 2, 4
```

---

## 🔹 Walrus operator `:=` (asignar dentro de la condición, Python ≥ 3.8)

```python
# En vez de:
lectura = obtener_lectura()
if lectura > 80:
    print(lectura)

# Se puede hacer en una línea:
if (lectura := obtener_lectura()) > 80:
    print(lectura)
```

Muy útil en bucles `while` para evitar repetir código:
```python
while (dato := input("Introduce valor (q para salir): ")) != "q":
    print(f"Procesando: {dato}")
```

---

## 🔹 Errores comunes

```python
# Olvidar los dos puntos
if temp > 80
    print("alerta")           # SyntaxError: falta ':'

# Indentación inconsistente (mezclar espacios y tabs)
if temp > 80:
    print("alerta")
   print("otra línea")        # IndentationError

# Confundir = con ==
if temp = 80:                  # SyntaxError

# Comparar con None usando ==
if valor == None:               # funciona, pero no recomendado
if valor is None:                 # ✅ recomendado

# elif después de un else (orden incorrecto)
if temp > 80:
    print("alto")
else:
    print("normal")
elif temp > 50:                  # SyntaxError: elif no puede ir después de else
    print("medio")
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Condicional básico | `if cond: ... elif cond2: ... else: ...` |
| Ternario en una línea | `x if cond else y` |
| Comprobar vacío | `if not lista:` |
| Comprobar None | `if valor is None:` |
| Comprobar rango | `if 0 < x < 100:` |
| Múltiples condiciones | `if cond1 and cond2:` |
| Switch-like | `match x: case 1: ... case _: ...` |
| Asignar y comparar a la vez | `if (n := funcion()) > 0:` |
| Saltar iteración en bucle | `continue` |
| Cortar bucle | `break` |
