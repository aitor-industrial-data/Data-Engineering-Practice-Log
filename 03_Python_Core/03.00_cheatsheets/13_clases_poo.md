# 📘 Python Datasheet — Clases y POO (Programación Orientada a Objetos)

---

## 🔹 Sintaxis básica

```python
class Sensor:
    def __init__(self, nombre, tipo, valor):     # constructor
        self.nombre = nombre                        # atributos de instancia
        self.tipo = tipo
        self.valor = valor

    def mostrar(self):                              # método
        return f"{self.nombre} ({self.tipo}): {self.valor}"

s1 = Sensor("T-101", "temperatura", 76.4)     # crear instancia (objeto)
s1.mostrar()                                     # "T-101 (temperatura): 76.4"
s1.valor                                           # acceso directo a atributo -> 76.4
```

📌 `self` representa la instancia actual. Es el primer parámetro de todo método de instancia, pero **no se pasa explícitamente** al llamar (`s1.mostrar()`, no `s1.mostrar(s1)`).

---

## 🔹 Atributos: instancia vs clase

```python
class Sensor:
    unidades = "SI"                    # atributo de CLASE -> compartido por todas las instancias

    def __init__(self, nombre, valor):
        self.nombre = nombre             # atributo de INSTANCIA -> propio de cada objeto
        self.valor = valor

s1 = Sensor("T-101", 76.4)
s2 = Sensor("T-102", 45.1)

s1.nombre          # "T-101"  -> distinto por instancia
s1.unidades          # "SI"     -> compartido
Sensor.unidades        # "SI"     -> accesible también desde la clase directamente

Sensor.unidades = "Métrico"     # cambia para TODAS las instancias
```

⚠️ **Gotcha:** igual que con listas en parámetros por defecto, si un atributo de clase es mutable (lista, dict), se comparte entre todas las instancias — cuidado.

---

## 🔹 Métodos: instancia, clase y estáticos

```python
class Sensor:
    contador = 0                            # atributo de clase

    def __init__(self, nombre):
        self.nombre = nombre
        Sensor.contador += 1

    def metodo_instancia(self):               # accede a self (datos del objeto)
        return f"Soy {self.nombre}"

    @classmethod
    def total_sensores(cls):                    # accede a la clase, no a la instancia
        return cls.contador

    @staticmethod
    def es_temperatura_valida(valor):              # no accede ni a self ni a cls
        return -50 <= valor <= 200

s1 = Sensor("T-101")
s2 = Sensor("T-102")

Sensor.total_sensores()                # 2
Sensor.es_temperatura_valida(300)         # False
```

| Tipo | Decorador | Primer parámetro | Uso típico |
|---|---|---|---|
| Instancia | (ninguno) | `self` | operar sobre datos del objeto |
| Clase | `@classmethod` | `cls` | crear instancias alternativas, contadores globales |
| Estático | `@staticmethod` | ninguno | función de utilidad relacionada temáticamente |

---

## 🔹 Herencia

```python
class SensorBase:
    def __init__(self, nombre):
        self.nombre = nombre

    def describir(self):
        return f"Sensor: {self.nombre}"

class SensorTemperatura(SensorBase):        # hereda de SensorBase
    def __init__(self, nombre, umbral):
        super().__init__(nombre)              # llama al __init__ de la clase padre
        self.umbral = umbral

    def describir(self):                        # sobrescribe el método del padre
        base = super().describir()                # reutiliza lógica del padre
        return f"{base} | Umbral: {self.umbral}"

st = SensorTemperatura("T-101", 80.0)
st.describir()          # "Sensor: T-101 | Umbral: 80.0"

isinstance(st, SensorBase)          # True -> SensorTemperatura ES un SensorBase
isinstance(st, SensorTemperatura)     # True
```

---

## 🔹 Métodos "mágicos" / dunder (`__init__`, `__str__`, etc.)

| Método | Se usa cuando... | Ejemplo de uso |
|---|---|---|
| `__init__` | crear la instancia | `Sensor("T-101")` |
| `__str__` | `print(obj)` o `str(obj)` | representación legible |
| `__repr__` | representación para debug (consola) | `repr(obj)` |
| `__len__` | `len(obj)` | tamaño del objeto |
| `__eq__` | `obj1 == obj2` | comparar por contenido |
| `__lt__` | `obj1 < obj2` | permite usar `sorted()` |
| `__getitem__` | `obj[i]` | indexado personalizado |

```python
class Sensor:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __str__(self):                     # se usa con print()
        return f"Sensor {self.nombre}: {self.valor}"

    def __repr__(self):                      # se usa en consola/debug
        return f"Sensor(nombre='{self.nombre}', valor={self.valor})"

    def __eq__(self, otro):                    # comparar por valor, no por identidad
        return self.valor == otro.valor

    def __lt__(self, otro):                      # permite sorted()
        return self.valor < otro.valor

s1 = Sensor("T-101", 76.4)
print(s1)                    # "Sensor T-101: 76.4"  (usa __str__)
s1                              # Sensor(nombre='T-101', valor=76.4)  (usa __repr__ en consola)

s2 = Sensor("T-102", 45.1)
s1 == s2                          # False (usa __eq__)
sorted([s1, s2])                    # ordena por valor (usa __lt__)
```

---

## 🔹 Encapsulación (convenciones, no forzado por el lenguaje)

```python
class Sensor:
    def __init__(self, nombre):
        self.nombre = nombre           # público -> acceso libre
        self._interno = 0                # "protegido" (convención: uso interno)
        self.__privado = "secreto"         # "privado" (name mangling)

s = Sensor("T-101")
s.nombre                       # ✅ acceso normal
s._interno                       # ⚠️ funciona, pero por convención no debería tocarse desde fuera
s.__privado                        # ❌ AttributeError (name mangling lo renombra internamente)
s._Sensor__privado                   # ✅ así sí se puede acceder (pero rompe la intención)
```

📌 Python no tiene atributos realmente privados como Java/C++. `_` y `__` son convenciones de "no tocar desde fuera", reforzadas técnicamente solo en el caso de `__`.

---

## 🔹 Properties (getters/setters pythónicos)

```python
class Sensor:
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):                    # se accede como atributo, no como método
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor):         # valida antes de asignar
        if nuevo_valor < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        self._valor = nuevo_valor

s = Sensor(76.4)
s.valor                    # 76.4 -> se llama como atributo, no s.valor()
s.valor = 80.0               # ejecuta el setter, valida internamente
s.valor = -500                 # ValueError
```

---

## 🔹 Dataclasses (forma moderna y rápida de crear clases con datos)

```python
from dataclasses import dataclass

@dataclass
class Sensor:
    nombre: str
    tipo: str
    valor: float
    activo: bool = True          # con valor por defecto

s = Sensor("T-101", "temperatura", 76.4)
s.nombre                            # "T-101"
print(s)                              # Sensor(nombre='T-101', tipo='temperatura', valor=76.4, activo=True)
# genera automáticamente __init__, __repr__ y __eq__
```

📌 Muy recomendable para clases que son principalmente "contenedores de datos" (como registros de un dataset) — ahorra mucho boilerplate frente a una clase tradicional.

---

## 🔹 Clases abstractas (definir una interfaz obligatoria)

```python
from abc import ABC, abstractmethod

class Sensor(ABC):
    @abstractmethod
    def leer(self):
        pass                          # obliga a que las clases hijas implementen este método

class SensorTemperatura(Sensor):
    def leer(self):
        return 76.4

# Sensor()                # ❌ TypeError: no se puede instanciar una clase abstracta
st = SensorTemperatura()      # ✅ funciona, implementa leer()
```

---

## 🔹 Errores comunes

```python
class Sensor:
    def __init__(nombre):          # ❌ falta 'self' como primer parámetro
        self.nombre = nombre

class Sensor:
    def mostrar():                   # ❌ falta 'self' -> TypeError al llamar s.mostrar()
        pass

# Atributo de clase mutable compartido sin querer
class Sensor:
    lecturas = []                       # ⚠️ compartido entre TODAS las instancias

    def agregar(self, valor):
        self.lecturas.append(valor)        # modifica la lista compartida, no una propia

s1 = Sensor()
s2 = Sensor()
s1.agregar(10)
print(s2.lecturas)                            # [10] <- ¡inesperado! comparten la misma lista

# Solución: inicializar listas/dicts en __init__
class Sensor:
    def __init__(self):
        self.lecturas = []            # ✅ cada instancia tiene su propia lista
```

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Definir clase | `class Nombre:` |
| Constructor | `def __init__(self, ...):` |
| Método de instancia | `def metodo(self):` |
| Método de clase | `@classmethod def m(cls):` |
| Método estático | `@staticmethod def m():` |
| Heredar de otra clase | `class Hija(Padre):` |
| Llamar al padre | `super().__init__(...)` |
| Representación con print | `def __str__(self):` |
| Comparar objetos | `def __eq__(self, otro):` |
| Getter/setter validado | `@property` / `@x.setter` |
| Clase rápida de datos | `@dataclass` |
| Forzar implementación en hijas | `@abstractmethod` (con `ABC`) |
