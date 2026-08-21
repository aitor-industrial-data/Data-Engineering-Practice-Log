# 📘 Python Datasheet — Strings (`str`)

Secuencia **inmutable** de caracteres. Cualquier "modificación" crea un string nuevo.

```python
texto = "Sensor T-101"
```

---

## 🔹 Crear y acceso

```python
simple      = 'texto'
doble       = "texto"
triple      = """texto
multilínea"""
raw         = r"C:\nuevo\archivo"      # ignora caracteres de escape (\n no es salto de línea)

s = "python"
s[0]           # 'p'
s[-1]           # 'n'
s[1:4]           # 'yth'
s[::-1]           # 'nohtyp' -> invertir string
len(s)              # 6
```

⚠️ **Inmutabilidad:** no puedes hacer `s[0] = "P"` → `TypeError`. Hay que crear un string nuevo.

---

## 🔹 f-strings (formateo moderno — usar siempre que se pueda)

```python
nombre = "T-101"
temp = 76.4

f"Sensor {nombre}: {temp}°C"                    # "Sensor T-101: 76.4°C"
f"{temp:.1f}"                                      # "76.4"  -> 1 decimal
f"{temp:.2f}"                                       # "76.40" -> 2 decimales
f"{temp:>10.1f}"                                     # alineado a la derecha, ancho 10
f"{1000000:,}"                                        # "1,000,000" -> separador de miles
f"{0.256:.1%}"                                          # "25.6%" -> porcentaje
f"{nombre!r}"                                             # "'T-101'" -> repr (con comillas)
f"{'texto' if temp > 50 else 'otro'}"                       # expresiones dentro de {}

# Debug rápido (Python 3.8+): muestra "variable=valor"
f"{temp=}"                                                   # "temp=76.4"
```

| Formato | Efecto | Ejemplo |
|---|---|---|
| `:.2f` | 2 decimales | `f"{3.14159:.2f}"` → `3.14` |
| `:,` | separador miles | `f"{1234567:,}"` → `1,234,567` |
| `:>10` | alinear derecha, ancho 10 | |
| `:<10` | alinear izquierda | |
| `:^10` | centrado | |
| `:05d` | rellenar con ceros | `f"{3:05d}"` → `00003` |
| `:.1%` | porcentaje | `f"{0.5:.1%}"` → `50.0%` |
| `:x` | hexadecimal | `f"{255:x}"` → `ff` |

---

## 🔹 Otros métodos de formateo (herencia, poco usados hoy)

```python
"Hola {}".format("mundo")               # "Hola mundo"
"Hola %s, tienes %d años" % ("Ana", 30)   # "Hola Ana, tienes 30 años"
```
📌 Preferir siempre **f-strings** salvo que trabajes con código legacy.

---

## 🔹 Métodos de transformación (devuelven string nuevo)

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.upper()` | mayúsculas | `"abc".upper()` → `"ABC"` |
| `.lower()` | minúsculas | `"ABC".lower()` → `"abc"` |
| `.title()` | Primera Letra Mayúscula | `"hola mundo".title()` → `"Hola Mundo"` |
| `.capitalize()` | solo primera letra | `"hola".capitalize()` → `"Hola"` |
| `.strip()` | quita espacios inicio/fin | `"  hola  ".strip()` → `"hola"` |
| `.lstrip()` / `.rstrip()` | quita solo por un lado | `"  hola".lstrip()` |
| `.replace(a, b)` | reemplaza substring | `"hola".replace("o","0")` → `"h0la"` |
| `.strip(chars)` | quita caracteres específicos | `"##hola##".strip("#")` → `"hola"` |

```python
"  Sensor T-101  ".strip()          # "Sensor T-101"
"sensor_temperatura".replace("_", " ")   # "sensor temperatura"
"CSV,con,comas".replace(",", ";")          # "CSV;con;comas"
```

---

## 🔹 Métodos de búsqueda / comprobación (devuelven bool o índice)

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.startswith(x)` | empieza con | `"T-101".startswith("T-")` → `True` |
| `.endswith(x)` | termina con | `"archivo.csv".endswith(".csv")` → `True` |
| `.find(x)` | índice (o -1 si no está) | `"hola".find("l")` → `2` |
| `.index(x)` | índice (error si no está) | `"hola".index("z")` → `ValueError` |
| `in` | pertenencia | `"lo" in "hola"` → `True` |
| `.count(x)` | cuenta ocurrencias | `"banana".count("a")` → `3` |
| `.isdigit()` | ¿solo dígitos? | `"123".isdigit()` → `True` |
| `.isalpha()` | ¿solo letras? | `"abc".isalpha()` → `True` |
| `.isalnum()` | ¿letras o números? | `"abc123".isalnum()` → `True` |
| `.isspace()` | ¿solo espacios? | `"  ".isspace()` → `True` |
| `.isupper()` / `.islower()` | ¿mayúsc/minúsc? | `"ABC".isupper()` → `True` |

```python
archivo = "datos_2026.csv"
archivo.endswith(".csv")            # True -> validar extensión de fichero

valor = "45.7"
valor.replace(".", "").isdigit()      # True -> comprobar si es numérico (truco común)
```

---

## 🔹 Dividir y unir (split / join) — muy usado en parsing

```python
linea = "T-101,temperatura,76.4,activo"

partes = linea.split(",")                    # ['T-101', 'temperatura', '76.4', 'activo']
palabras = "hola mundo python".split()          # split() sin args -> por espacios: ['hola','mundo','python']
lineas = "linea1\nlinea2\nlinea3".splitlines()     # ['linea1', 'linea2', 'linea3']

# join -> inverso de split, MUY usado (nótese que se llama sobre el separador)
",".join(["T-101", "temperatura", "76.4"])      # "T-101,temperatura,76.4"
" ".join(["hola", "mundo"])                       # "hola mundo"
```

📌 **Patrón clásico de parsing CSV manual:**
```python
linea = "T-101,76.4,activo"
nombre, temp, estado = linea.split(",")
temp = float(temp)
```

---

## 🔹 Slicing avanzado

```python
s = "python"
s[1:4]         # 'yth'
s[:3]           # 'pyt'
s[3:]           # 'hon'
s[::2]           # 'pto'  -> de 2 en 2
s[::-1]           # 'nohtyp' -> invertir
s[-3:]             # 'hon' -> últimos 3
```

---

## 🔹 Concatenar y repetir

```python
a = "hola"
b = "mundo"
c = a + " " + b          # "hola mundo"
d = a * 3                  # "holaholahola"

# Concatenar muchos strings -> mejor con join que con + en un bucle (rendimiento)
partes = ["a", "b", "c", "d"]
resultado = "".join(partes)     # eficiente
# vs
resultado = ""
for p in partes:
    resultado += p                # ineficiente en bucles grandes (crea string nuevo cada vez)
```

---

## 🔹 Multilínea y escapes

```python
texto = "Línea 1\nLínea 2\tTabulado"     # \n salto de línea, \t tabulación
texto_multi = """
Línea 1
Línea 2
"""

raw = r"C:\Users\nombre"                    # raw string, ignora \n, \t, etc.
comillas = "Dice \"hola\""                     # escapar comillas
comillas = 'Dice "hola"'                          # o usar comillas distintas
```

---

## 🔹 Comprobar / limpiar datos (muy común al leer ficheros)

```python
valor_raw = "  76.4 \n"
valor_limpio = valor_raw.strip()               # "76.4"
valor_num = float(valor_limpio)                  # 76.4

# Validar antes de convertir
texto = "45.7"
if texto.replace(".", "", 1).isdigit():
    valor = float(texto)
```

---

## 🔹 Errores comunes

```python
s = "hola"
s[0] = "H"                      # TypeError: strings son inmutables

int("45.7")                       # ValueError -> usar float() primero
int("abc")                          # ValueError -> no es numérico

"hola".find("z")                      # -1 (no error, pero hay que comprobarlo)
"hola".index("z")                       # ValueError (sí da error)

# Concatenar tipos distintos sin convertir
"Valor: " + 45                            # TypeError
"Valor: " + str(45)                         # ✅
f"Valor: {45}"                                # ✅ f-strings convierten automáticamente
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Formatear con variables | `f"{variable}"` |
| Formatear decimales | `f"{valor:.2f}"` |
| Quitar espacios | `s.strip()` |
| Dividir por separador | `s.split(",")` |
| Unir lista en string | `",".join(lista)` |
| Reemplazar texto | `s.replace(a, b)` |
| Comprobar inicio/fin | `s.startswith(x)` / `s.endswith(x)` |
| Buscar posición | `s.find(x)` |
| Mayúsculas/minúsculas | `s.upper()` / `s.lower()` |
| Comprobar si es numérico | `s.replace(".","",1).isdigit()` |
| Invertir string | `s[::-1]` |
