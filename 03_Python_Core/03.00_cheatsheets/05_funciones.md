# 📘 Python Datasheet — Funciones (def)

---

## 🔹 Sintaxis básica

```python
def nombre_funcion(parametros):
    """Docstring opcional pero recomendada"""
    # cuerpo
    return resultado
```

```python
def sumar(a, b):
    return a + b

resultado = sumar(3, 5)      # 8

def saludar():                 # sin parámetros
    print("Hola")

def sin_return():               # sin return explícito
    print("hola")
valor = sin_return()             # valor = None
```

---

## 🔹 Parámetros: posicionales, por defecto, keyword

| Tipo | Sintaxis | Ejemplo llamada |
|---|---|---|
| Posicional | `def f(a, b):` | `f(1, 2)` |
| Por defecto | `def f(a, b=10):` | `f(1)` o `f(1, 20)` |
| Keyword (nombrado) | `def f(a, b):` | `f(b=2, a=1)` |
| Solo keyword (forzado) | `def f(a, *, b):` | `f(1, b=2)` (obligatorio nombrar `b`) |
| Solo posicional (forzado) | `def f(a, b, /):` | `f(1, 2)` (no se puede `f(a=1,b=2)`) |

```python
def crear_sensor(nombre, tipo="temperatura", activo=True):
    return f"{nombre} ({tipo}) - Activo: {activo}"

crear_sensor("T-101")                              # usa defaults
crear_sensor("T-101", "presion")                     # posicional
crear_sensor("T-101", activo=False)                   # keyword, salta el 2º
crear_sensor(nombre="T-101", tipo="vibracion")          # todo keyword
```

⚠️ **Gotcha clásico:** nunca uses un objeto mutable (`list`, `dict`) como valor por defecto:
```python
def mal(lista=[]):              # ❌ PELIGRO: la lista persiste entre llamadas
    lista.append(1)
    return lista

mal()    # [1]
mal()    # [1, 1]  <- ¡inesperado! la misma lista se reutiliza

def bien(lista=None):            # ✅ patrón correcto
    if lista is None:
        lista = []
    lista.append(1)
    return lista
```

---

## 🔹 `*args` y `**kwargs`

```python
def sumar_todo(*args):              # args llega como tupla
    return sum(args)

sumar_todo(1, 2, 3, 4)                # 10

def mostrar_info(**kwargs):           # kwargs llega como diccionario
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

mostrar_info(nombre="T-101", tipo="temperatura")

def funcion_completa(a, b, *args, c=10, **kwargs):
    print(a, b, args, c, kwargs)

funcion_completa(1, 2, 3, 4, c=99, extra="dato")
# 1 2 (3, 4) 99 {'extra': 'dato'}
```

| Símbolo | Significa | Recibe |
|---|---|---|
| `*args` | número variable de posicionales | tupla |
| `**kwargs` | número variable de keyword args | diccionario |
| `*lista` (al llamar) | desempaquetar lista como args | — |
| `**dict` (al llamar) | desempaquetar dict como kwargs | — |

```python
# Desempaquetar al LLAMAR una función
valores = [1, 2, 3]
sumar_todo(*valores)              # equivale a sumar_todo(1, 2, 3)

datos = {"nombre": "T-101", "tipo": "temp"}
mostrar_info(**datos)               # equivale a mostrar_info(nombre="T-101", tipo="temp")
```

---

## 🔹 `return` — comportamiento

```python
def clasificar(temp):
    if temp > 90:
        return "crítico"
    return "normal"           # solo se ejecuta si no hubo return antes

def multiples_valores():
    return 1, 2, 3              # en realidad devuelve una tupla (1,2,3)

a, b, c = multiples_valores()     # desempaquetado directo

def sin_return():
    pass
print(sin_return())              # None -> toda función sin return explícito devuelve None
```

---

## 🔹 Scope (ámbito de variables)

```python
x = 10                    # variable global

def modificar():
    x = 20                  # variable LOCAL, distinta a la global
    print(x)                 # 20

modificar()
print(x)                     # 10 -> la global no cambió

def modificar_global():
    global x                  # declara que quieres modificar la global
    x = 20

modificar_global()
print(x)                       # 20
```

| Palabra clave | Uso |
|---|---|
| `global` | modificar variable global desde dentro de una función |
| `nonlocal` | modificar variable de función envolvente (closures) |

```python
def externa():
    contador = 0
    def interna():
        nonlocal contador
        contador += 1
        return contador
    return interna

incrementar = externa()
incrementar()      # 1
incrementar()       # 2  -> recuerda el estado (closure)
```

---

## 🔹 Funciones lambda (anónimas)

```python
cuadrado = lambda x: x**2
cuadrado(5)               # 25

suma = lambda a, b: a + b
suma(3, 4)                  # 7

# Uso típico: como argumento de otras funciones
sorted([3,1,2], key=lambda x: -x)          # [3,2,1]
list(map(lambda x: x*2, [1,2,3]))            # [2,4,6]
list(filter(lambda x: x > 1, [1,2,3]))        # [2,3]
```

📌 Usa `lambda` solo para funciones simples de una línea. Si necesita más lógica, mejor `def`.

---

## 🔹 Type hints (anotaciones de tipo, opcional pero recomendado)

```python
def sumar(a: int, b: int) -> int:
    return a + b

def procesar(nombre: str, valores: list[float], activo: bool = True) -> dict:
    return {"nombre": nombre, "media": sum(valores)/len(valores)}

# No son obligatorios ni se validan en tiempo de ejecución,
# pero ayudan mucho a la legibilidad y a herramientas como mypy/IDEs
```

---

## 🔹 Docstrings (documentación de funciones)

```python
def calcular_media(valores: list[float]) -> float:
    """
    Calcula la media aritmética de una lista de valores.

    Args:
        valores: lista de números.

    Returns:
        La media como float.
    """
    return sum(valores) / len(valores)

calcular_media.__doc__       # accede al docstring
help(calcular_media)          # muestra la ayuda formateada
```

---

## 🔹 Funciones como objetos de primera clase

```python
def cuadrado(x):
    return x**2

def aplicar(funcion, valor):        # se puede pasar una función como argumento
    return funcion(valor)

aplicar(cuadrado, 5)                  # 25

operaciones = {                        # se puede guardar en diccionarios
    "suma": lambda a, b: a+b,
    "resta": lambda a, b: a-b
}
operaciones["suma"](3, 4)               # 7
```

---

## 🔹 Recursividad

```python
def factorial(n):
    if n <= 1:                 # caso base -> imprescindible o bucle infinito
        return 1
    return n * factorial(n - 1)   # llamada recursiva

factorial(5)     # 120
```

⚠️ Python tiene un límite de recursión (por defecto ~1000). Para bucles muy profundos, mejor iterativo.

---

## 🔹 Errores comunes

```python
# Objeto mutable como valor por defecto (ver arriba)
def mal(lista=[]): ...

# Confundir return con print
def suma(a, b):
    print(a + b)          # imprime pero NO devuelve nada
resultado = suma(2, 3)      # resultado = None

# Olvidar self en métodos de clase (se verá en la página de POO)

# Llamar función antes de definirla
resultado = f()               # NameError si f() se define después en el script
def f():
    return 1

# Mezclar posicional después de keyword
def f(a, b): pass
f(a=1, 2)                     # SyntaxError: positional argument follows keyword argument
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Definir función | `def f(a, b): return a+b` |
| Parámetro por defecto | `def f(a, b=10):` |
| Número variable de args | `def f(*args):` |
| Número variable de kwargs | `def f(**kwargs):` |
| Desempaquetar al llamar | `f(*lista)` / `f(**dict)` |
| Función de una línea | `lambda x: x**2` |
| Modificar variable global | `global x` |
| Modificar variable de closure | `nonlocal x` |
| Anotar tipos | `def f(a: int) -> int:` |
| Documentar función | `"""docstring"""` tras el `def` |
