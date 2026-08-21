# 📘 Python Datasheet — Ficheros (open, with, lectura/escritura)

---

## 🔹 Abrir ficheros — `open()`

```python
f = open("datos.txt", "r")     # abrir en modo lectura
contenido = f.read()
f.close()                        # ⚠️ hay que cerrarlo manualmente
```

📌 **Mejor práctica siempre:** usar `with`, que cierra el fichero automáticamente incluso si hay un error.

```python
with open("datos.txt", "r") as f:
    contenido = f.read()
# el fichero ya está cerrado aquí, aunque haya habido una excepción dentro del bloque
```

---

## 🔹 Modos de apertura

| Modo | Significado |
|---|---|
| `"r"` | lectura (por defecto). Error si el fichero no existe |
| `"w"` | escritura. **Sobrescribe** el fichero completo (o lo crea) |
| `"a"` | append. Añade al final sin borrar lo existente |
| `"x"` | crea el fichero, error si ya existe |
| `"r+"` | lectura y escritura |
| `"rb"` / `"wb"` | modo binario (imágenes, PDFs, etc.) |

```python
with open("log.txt", "a") as f:      # añadir sin borrar lo anterior
    f.write("Nueva línea\n")

with open("nuevo.txt", "x") as f:      # falla si "nuevo.txt" ya existe
    f.write("contenido")
```

⚠️ **Gotcha crítico:** abrir con `"w"` **borra todo el contenido anterior** del fichero, aunque no escribas nada. Si quieres conservar lo existente, usa `"a"`.

---

## 🔹 Leer ficheros

| Método | Qué hace |
|---|---|
| `.read()` | todo el contenido como un único string |
| `.readline()` | una línea (incluye `\n`) |
| `.readlines()` | lista con todas las líneas |
| iterar directo (`for linea in f`) | recorre línea a línea (más eficiente en memoria) |

```python
with open("datos.txt", "r") as f:
    contenido = f.read()            # todo el fichero de golpe

with open("datos.txt", "r") as f:
    lineas = f.readlines()             # ['linea1\n', 'linea2\n', ...]

with open("datos.txt", "r") as f:
    primera = f.readline()               # solo la primera línea

# Forma más eficiente para ficheros grandes (no carga todo en memoria)
with open("datos.txt", "r") as f:
    for linea in f:
        linea = linea.strip()               # quitar el \n del final
        print(linea)
```

📌 **Para Data Engineering:** con ficheros grandes (logs, CSVs de millones de filas), siempre iterar línea a línea (`for linea in f`) en vez de `.read()` o `.readlines()`, que cargan todo en memoria de golpe.

---

## 🔹 Escribir ficheros

```python
with open("salida.txt", "w") as f:
    f.write("Primera línea\n")
    f.write("Segunda línea\n")

# Escribir varias líneas de una vez desde una lista
lineas = ["linea1\n", "linea2\n", "linea3\n"]
with open("salida.txt", "w") as f:
    f.writelines(lineas)          # ⚠️ NO añade \n automáticamente, hay que incluirlo tú

# print() también puede escribir directo a fichero
with open("salida.txt", "w") as f:
    print("Hola mundo", file=f)     # print SÍ añade salto de línea automático
```

---

## 🔹 Codificación (encoding) — evitar errores con tildes/ñ

```python
# En Windows especialmente, especificar encoding evita UnicodeDecodeError
with open("datos.txt", "r", encoding="utf-8") as f:
    contenido = f.read()

with open("salida.txt", "w", encoding="utf-8") as f:
    f.write("Configuración eléctrica: cuadro de mando")
```

📌 **Recomendación:** especifica siempre `encoding="utf-8"` explícitamente, sobre todo si el texto tiene tildes, eñes o caracteres especiales — evita bugs difíciles de depurar entre sistemas operativos distintos.

---

## 🔹 Comprobar si un fichero existe

```python
import os
from pathlib import Path

os.path.exists("datos.txt")            # True/False (forma clásica)

Path("datos.txt").exists()               # True/False (forma moderna, recomendada)
Path("datos.txt").is_file()                # comprueba que es fichero (no carpeta)
```

---

## 🔹 Trabajar con rutas — `pathlib` (forma moderna recomendada)

```python
from pathlib import Path

ruta = Path("datos") / "sensores" / "2026" / "enero.csv"    # construir ruta multiplataforma
ruta.exists()                    # comprobar existencia
ruta.name                          # "enero.csv"
ruta.suffix                          # ".csv"
ruta.stem                              # "enero" (sin extensión)
ruta.parent                              # Path("datos/sensores/2026")

# Listar ficheros de una carpeta
for fichero in Path("datos").glob("*.csv"):     # todos los .csv del directorio
    print(fichero)

for fichero in Path("datos").rglob("*.csv"):      # recursivo, incluye subcarpetas
    print(fichero)

# Crear carpetas
Path("nueva_carpeta").mkdir(exist_ok=True)          # exist_ok evita error si ya existe
Path("a/b/c").mkdir(parents=True, exist_ok=True)       # crea toda la ruta intermedia
```

---

## 🔹 CSV — lectura y escritura con el módulo `csv`

```python
import csv

# Leer CSV como listas
with open("sensores.csv", "r", encoding="utf-8") as f:
    lector = csv.reader(f)
    cabecera = next(lector)              # primera fila = cabecera
    for fila in lector:
        print(fila)                        # cada fila es una lista de strings

# Leer CSV como diccionarios (más legible, usa la cabecera como claves)
with open("sensores.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        print(fila["nombre"], fila["valor"])    # acceso por nombre de columna

# Escribir CSV
with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(["nombre", "tipo", "valor"])         # cabecera
    escritor.writerow(["T-101", "temperatura", 76.4])

# Escribir CSV desde diccionarios
datos = [{"nombre": "T-101", "valor": 76.4}, {"nombre": "T-102", "valor": 45.1}]
with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=["nombre", "valor"])
    escritor.writeheader()
    escritor.writerows(datos)
```

⚠️ **Gotcha en Windows:** al escribir CSV, usar `newline=""` en `open()` evita líneas en blanco duplicadas entre filas.

---

## 🔹 JSON — lectura y escritura

```python
import json

# Leer JSON desde fichero
with open("config.json", "r", encoding="utf-8") as f:
    datos = json.load(f)                # dict o list de Python

# Escribir JSON a fichero
config = {"nombre": "T-101", "umbral": 80.0, "activo": True}
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)     # indent=2 -> legible; ensure_ascii=False -> conserva tildes/ñ

# Convertir entre string JSON y objeto Python (sin fichero)
texto_json = json.dumps(config, indent=2)      # dict -> string JSON
objeto = json.loads(texto_json)                   # string JSON -> dict
```

---

## 🔹 Múltiples ficheros a la vez

```python
with open("entrada.csv") as f_in, open("salida.csv", "w") as f_out:
    for linea in f_in:
        f_out.write(linea.upper())
```

---

## 🔹 Errores comunes

```python
f = open("datos.txt")
# ... si algo falla aquí, el fichero nunca se cierra
f.close()

# Solución: usar siempre with
with open("datos.txt") as f:
    pass          # se cierra automáticamente, incluso con excepción

# Abrir en "w" borra todo sin avisar
with open("importante.txt", "w") as f:      # ⚠️ ¡esto vacía el fichero al instante!
    pass

# Olvidar encoding -> errores con tildes en algunos sistemas
open("datos.txt")                              # puede fallar con ñ/tildes en Windows
open("datos.txt", encoding="utf-8")              # ✅ más seguro

# Fichero no encontrado sin gestionar
with open("no_existe.txt") as f:                   # FileNotFoundError
    pass
# Mejor con manejo de errores (ver página 11)
try:
    with open("no_existe.txt") as f:
        pass
except FileNotFoundError:
    print("El fichero no existe")
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Abrir y cerrar automáticamente | `with open("f.txt") as f:` |
| Leer todo | `f.read()` |
| Leer línea a línea (eficiente) | `for linea in f:` |
| Escribir (sobrescribe) | `open("f.txt", "w")` |
| Añadir sin borrar | `open("f.txt", "a")` |
| Comprobar si existe | `Path("f.txt").exists()` |
| Listar ficheros de carpeta | `Path("dir").glob("*.csv")` |
| Leer CSV como dict | `csv.DictReader(f)` |
| Leer JSON | `json.load(f)` |
| Escribir JSON legible | `json.dump(d, f, indent=2)` |
