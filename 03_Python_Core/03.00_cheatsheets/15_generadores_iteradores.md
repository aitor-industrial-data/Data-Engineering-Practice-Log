# 📘 Python Datasheet — Generadores e Iteradores

---

## 🔹 Iterable vs Iterador vs Generador (diferencias clave)

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Iterable** | objeto que se puede recorrer con `for` | lista, tupla, dict, str, set |
| **Iterador** | objeto que produce valores uno a uno con `next()` | resultado de `iter(lista)` |
| **Generador** | forma sencilla de crear un iterador con `yield` o `()` | función con `yield`, generator expression |

```python
lista = [1, 2, 3]              # iterable
iterador = iter(lista)           # iterador -> tiene estado, recuerda por dónde va
next(iterador)                     # 1
next(iterador)                       # 2
next(iterador)                         # 3
next(iterador)                           # StopIteration -> ya no quedan elementos
```

📌 Un `for` internamente hace esto automáticamente: llama a `iter()` y luego `next()` repetidamente hasta capturar `StopIteration`.

---

## 🔹 Generator expressions (la forma más simple)

```python
cuadrados = (x**2 for x in range(1000000))    # NO calcula nada todavía (perezoso/lazy)

next(cuadrados)          # 0  -> calcula solo el primero
next(cuadrados)            # 1  -> calcula solo el siguiente

# Recorrer con for (consume el generador)
for valor in (x**2 for x in range(5)):
    print(valor)

suma = sum(x**2 for x in range(1000000))       # eficiente en memoria: no crea lista completa
```

| Sintaxis | Tipo | Memoria |
|---|---|---|
| `[x**2 for x in range(n)]` | list comprehension | carga TODO en memoria |
| `(x**2 for x in range(n))` | generator expression | calcula uno a uno, bajo consumo |

---

## 🔹 Funciones generadoras (`yield`)

```python
def contador(hasta):
    n = 1
    while n <= hasta:
        yield n              # "pausa" aquí y devuelve n, recuerda el estado
        n += 1

gen = contador(3)
next(gen)      # 1
next(gen)        # 2
next(gen)          # 3
next(gen)            # StopIteration

for numero in contador(5):    # se puede recorrer directamente con for
    print(numero)              # 1, 2, 3, 4, 5
```

📌 **Diferencia clave con `return`:** `return` termina la función y devuelve un valor final. `yield` "pausa" la función, devuelve un valor, y **recuerda el estado** para continuar en la siguiente llamada a `next()`.

```python
def leer_lineas_grandes(ruta):
    """Generador para leer ficheros enormes sin cargarlos enteros en memoria"""
    with open(ruta) as f:
        for linea in f:
            yield linea.strip()

for linea in leer_lineas_grandes("log_gigante.txt"):
    procesar(linea)          # procesa una línea cada vez, sin cargar todo el fichero
```

---

## 🔹 Varios `yield` en la misma función

```python
def secuencia():
    yield "inicio"
    yield "proceso"
    yield "fin"

list(secuencia())      # ['inicio', 'proceso', 'fin']
```

---

## 🔹 `yield from` — delegar en otro generador

```python
def sub_generador():
    yield 1
    yield 2

def generador_principal():
    yield "inicio"
    yield from sub_generador()      # delega, equivale a repetir yield para cada valor
    yield "fin"

list(generador_principal())          # ['inicio', 1, 2, 'fin']
```

---

## 🔹 Ventajas de los generadores (por qué usarlos)

| Ventaja | Explicación |
|---|---|
| Memoria eficiente | no genera todos los valores de golpe, solo cuando se piden |
| Evaluación perezosa (lazy) | los cálculos se hacen "just in time" |
| Ideal para streams/ficheros grandes | procesa dato a dato sin cargar todo |
| Puede representar secuencias infinitas | (no tendría sentido con una lista) |

```python
# Secuencia infinita -> imposible con una lista normal
def naturales():
    n = 0
    while True:
        yield n
        n += 1

gen = naturales()
next(gen)     # 0
next(gen)       # 1
next(gen)         # 2   -> podría seguir para siempre, sin problema de memoria

# Cortar una secuencia infinita con itertools
from itertools import islice
primeros_10 = list(islice(naturales(), 10))      # [0,1,2,...,9]
```

---

## 🔹 Generadores se "agotan" (se consumen una sola vez)

```python
gen = (x for x in range(3))

list(gen)          # [0, 1, 2]
list(gen)            # []  <- ¡ya está vacío! los generadores no se pueden reiniciar

# Si necesitas recorrerlo varias veces, usa una lista o vuelve a crear el generador
gen_lista = list(x for x in range(3))
list(gen_lista)          # se puede recorrer las veces que quieras
```

⚠️ **Gotcha muy común:** intentar reutilizar un generador ya recorrido no da error, simplemente no devuelve nada más.

---

## 🔹 `map()`, `filter()` — devuelven objetos "lazy" similares a generadores

```python
datos = [1, 2, 3, 4, 5]

dobles = map(lambda x: x*2, datos)        # objeto map, no lista (lazy)
list(dobles)                                 # [2,4,6,8,10] -> hay que convertir para ver el resultado

pares = filter(lambda x: x % 2 == 0, datos)   # objeto filter, lazy
list(pares)                                      # [2, 4]
```

---

## 🔹 Crear un iterador personalizado (clase con `__iter__`/`__next__`)

```python
class Contador:
    def __init__(self, hasta):
        self.actual = 0
        self.hasta = hasta

    def __iter__(self):          # debe devolver un objeto con __next__
        return self

    def __next__(self):
        if self.actual >= self.hasta:
            raise StopIteration     # señal de fin, igual que los generadores internamente
        self.actual += 1
        return self.actual

for numero in Contador(3):
    print(numero)      # 1, 2, 3
```

📌 En la práctica, casi siempre es más simple usar una función generadora (`yield`) que definir una clase con `__iter__`/`__next__` a mano — Python hace el trabajo pesado por ti.

---

## 🔹 Comparativa rápida: list comprehension vs generador

```python
# List comprehension -> todo en memoria, se puede recorrer varias veces, tiene len()
cuadrados_lista = [x**2 for x in range(1000)]
len(cuadrados_lista)                              # 1000 -> funciona

# Generator expression -> memoria mínima, un solo uso, NO tiene len()
cuadrados_gen = (x**2 for x in range(1000))
len(cuadrados_gen)                                   # TypeError: generators no tienen len()
```

| Usar... | Cuándo |
|---|---|
| List comprehension | necesitas la lista completa, recorrerla varias veces, o su longitud |
| Generator expression | solo vas a recorrerla una vez, dataset grande, quieres ahorrar memoria |

---

## 🔹 Errores comunes

```python
gen = (x for x in range(5))
list(gen)      # [0,1,2,3,4]
list(gen)        # []  <- generador ya agotado

def mi_generador():
    return 1          # ❌ esto NO es un generador si no tiene yield en ningún punto
    yield 2              # (código inalcanzable en este caso, pero conceptualmente:
                            #  basta con que exista un yield en la función para que TODA
                            #  la función se convierta en generadora)

next(iter([1,2,3]))       # 1 -> ok
next([1,2,3])                # TypeError: una lista no es un iterador, hay que envolverla en iter()
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Crear generador con función | `def f(): yield x` |
| Generator expression | `(x for x in iterable)` |
| Obtener siguiente valor | `next(generador)` |
| Convertir iterable en iterador | `iter(lista)` |
| Delegar en otro generador | `yield from otro_gen()` |
| Cortar secuencia infinita | `itertools.islice(gen, n)` |
| Transformar de forma lazy | `map(f, iterable)` |
| Filtrar de forma lazy | `filter(cond, iterable)` |
| Iterador personalizado | clase con `__iter__` + `__next__` |
