# 📘 Python Datasheet — Módulos e Imports

---

## 🔹 ¿Qué es un módulo?

Cualquier fichero `.py` es un módulo. Un conjunto de módulos en una carpeta con `__init__.py` (opcional desde Python 3.3+) es un **paquete**.

```
proyecto/
├── main.py
├── utils.py              # módulo
└── procesamiento/         # paquete
    ├── __init__.py
    ├── limpieza.py
    └── validacion.py
```

---

## 🔹 Formas de importar

```python
import math                          # importa el módulo completo
math.sqrt(16)                          # hay que usar el prefijo math.

import math as m                       # con alias
m.sqrt(16)

from math import sqrt                    # importa solo una función
sqrt(16)                                   # sin prefijo

from math import sqrt, pi                  # varias funciones específicas

from math import sqrt as raiz                # función con alias

from math import *                             # importa TODO (⚠️ evitar, ver abajo)
```

⚠️ **Gotcha:** `from modulo import *` contamina el espacio de nombres global y puede sobrescribir funciones sin avisar. Evitar en código serio; usar imports explícitos.

---

## 🔹 Importar módulos propios

```python
# utils.py
def limpiar_texto(texto):
    return texto.strip().lower()

# main.py (mismo directorio)
import utils
utils.limpiar_texto("  HOLA  ")

from utils import limpiar_texto
limpiar_texto("  HOLA  ")
```

```python
# Desde un paquete (carpeta con __init__.py)
from procesamiento.limpieza import limpiar_texto
from procesamiento import limpieza
limpieza.limpiar_texto("texto")
```

---

## 🔹 `if __name__ == "__main__"` — patrón imprescindible

```python
# archivo: procesar.py
def procesar_datos(datos):
    return [x * 2 for x in datos]

def main():
    resultado = procesar_datos([1, 2, 3])
    print(resultado)

if __name__ == "__main__":
    main()
```

📌 **Por qué importa:** el código dentro de `if __name__ == "__main__":` solo se ejecuta si el fichero se corre directamente (`python procesar.py`), NO si se importa desde otro fichero (`import procesar`). Esto permite reutilizar funciones sin que se ejecute lógica "de prueba" automáticamente al importar.

```python
# Sin esta protección, importar el módulo ejecutaría main() sin querer:
import procesar          # si no hubiera if __name__..., esto imprimiría [2,4,6] al importar
```

---

## 🔹 Módulos estándar más usados (referencia rápida)

| Módulo | Para qué sirve |
|---|---|
| `os` | rutas, variables de entorno, sistema operativo |
| `sys` | argumentos de línea de comandos, salida del script |
| `pathlib` | manejo moderno de rutas de ficheros |
| `datetime` | fechas y horas |
| `json` | leer/escribir JSON |
| `csv` | leer/escribir CSV |
| `re` | expresiones regulares |
| `math` | funciones matemáticas |
| `random` | números aleatorios |
| `collections` | `Counter`, `defaultdict`, `namedtuple` |
| `itertools` | combinaciones, productos, iteradores avanzados |
| `functools` | `reduce`, `lru_cache`, decoradores útiles |
| `logging` | logs estructurados (mejor que `print` en producción) |
| `time` | medir tiempos, pausas (`sleep`) |
| `argparse` | parsear argumentos de terminal |

```python
import os
os.getcwd()                     # directorio actual
os.environ.get("HOME")           # variable de entorno

import sys
sys.argv                          # lista de argumentos pasados al script
sys.exit(1)                         # termina el script con código de salida

from datetime import datetime, timedelta
ahora = datetime.now()
manana = ahora + timedelta(days=1)

import re
re.findall(r"\d+", "T-101 tiene 76.4 grados")     # ['101', '76', '4']

import time
time.sleep(2)                       # pausa 2 segundos
inicio = time.time()                  # timestamp actual (para medir duración)
```

---

## 🔹 Entornos virtuales e instalación de paquetes (contexto rápido)

```bash
# Crear entorno virtual
python -m venv venv

# Activarlo
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate             # Windows

# Instalar paquetes de terceros
pip install pandas numpy requests

# Guardar dependencias del proyecto
pip freeze > requirements.txt

# Instalar desde ese fichero (en otra máquina/entorno)
pip install -r requirements.txt
```

```python
# Una vez instalados, se importan igual que los módulos estándar
import pandas as pd
import numpy as np
import requests
```

---

## 🔹 Import relativo vs absoluto (dentro de paquetes)

```python
# Estructura:
# proyecto/
# ├── main.py
# └── procesamiento/
#     ├── __init__.py
#     ├── limpieza.py
#     └── validacion.py

# Import absoluto (recomendado, más claro)
from procesamiento.limpieza import limpiar_texto

# Import relativo (dentro de validacion.py, para importar limpieza.py del mismo paquete)
from .limpieza import limpiar_texto      # el punto indica "mismo nivel de paquete"
from ..otro_paquete import algo             # dos puntos = un nivel arriba
```

---

## 🔹 `__init__.py` — controlar qué se expone del paquete

```python
# procesamiento/__init__.py
from .limpieza import limpiar_texto
from .validacion import validar_esquema

# Ahora desde fuera se puede hacer directamente:
from procesamiento import limpiar_texto, validar_esquema
# en vez de:
from procesamiento.limpieza import limpiar_texto
```

---

## 🔹 Recargar un módulo modificado (útil en notebooks/REPL)

```python
import importlib
import mi_modulo

importlib.reload(mi_modulo)     # fuerza recarga sin reiniciar el intérprete
```

---

## 🔹 Errores comunes

```python
import modulo_que_no_existe        # ModuleNotFoundError

from math import raiz_cuadrada       # ImportError: no existe esa función en math

# Import circular: A importa de B y B importa de A -> error
# Solución: reestructurar código o mover el import dentro de la función

# Ejecutar código de nivel superior sin protección __main__
# (esto se ejecuta SIEMPRE, incluso al importar el módulo desde otro lado)
print("Este script se está ejecutando")    # ⚠️ se dispara también al hacer import

# Nombre de fichero propio que coincide con un módulo estándar
# archivo llamado random.py en tu proyecto -> rompe "import random" en cualquier fichero del proyecto
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Importar módulo completo | `import modulo` |
| Importar con alias | `import modulo as m` |
| Importar función concreta | `from modulo import funcion` |
| Evitar ejecución al importar | `if __name__ == "__main__":` |
| Ver directorio actual | `os.getcwd()` |
| Argumentos de terminal | `sys.argv` |
| Instalar paquete | `pip install nombre` |
| Congelar dependencias | `pip freeze > requirements.txt` |
| Import dentro de paquete | `from .modulo import funcion` |
