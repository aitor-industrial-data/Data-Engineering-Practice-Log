# 📘 Python Datasheet — Manejo de Errores (try / except)

---

## 🔹 Sintaxis básica

```python
try:
    # código que puede fallar
except TipoError:
    # qué hacer si falla
else:
    # se ejecuta SOLO si no hubo error
finally:
    # se ejecuta SIEMPRE, haya error o no
```

```python
try:
    valor = int("abc")
except ValueError:
    print("No se pudo convertir")
# No se pudo convertir
```

---

## 🔹 Excepciones más comunes

| Excepción | Cuándo ocurre |
|---|---|
| `ValueError` | valor de tipo correcto pero inválido (`int("abc")`) |
| `TypeError` | operación entre tipos incompatibles (`"a" + 1`) |
| `KeyError` | clave no existe en un diccionario |
| `IndexError` | índice fuera de rango en lista/tupla |
| `AttributeError` | método/atributo no existe (`None.append()`) |
| `ZeroDivisionError` | división entre 0 |
| `FileNotFoundError` | fichero no encontrado al abrir |
| `ImportError` / `ModuleNotFoundError` | módulo no encontrado al importar |
| `NameError` | variable no definida |
| `StopIteration` | fin de un iterador |

```python
try:
    d = {"a": 1}
    d["b"]
except KeyError:
    print("Clave no encontrada")

try:
    l = [1, 2, 3]
    l[10]
except IndexError:
    print("Índice fuera de rango")
```

---

## 🔹 Capturar varias excepciones

```python
try:
    valor = int(input("Número: "))
    resultado = 10 / valor
except ValueError:
    print("Eso no es un número")
except ZeroDivisionError:
    print("No se puede dividir entre 0")

# Varias excepciones en un solo except
try:
    pass
except (ValueError, TypeError) as e:
    print(f"Error: {e}")

# Capturar todo (usar con cuidado, poco específico)
try:
    pass
except Exception as e:
    print(f"Error inesperado: {e}")
```

⚠️ **Gotcha:** nunca uses `except:` a secas (sin especificar tipo) — captura hasta `KeyboardInterrupt` y `SystemExit`, lo cual puede ocultar bugs graves. Usa `except Exception:` como mínimo.

---

## 🔹 Acceder al mensaje de error

```python
try:
    int("abc")
except ValueError as e:
    print(e)                    # invalid literal for int() with base 10: 'abc'
    print(type(e).__name__)       # ValueError
```

---

## 🔹 `else` y `finally`

```python
try:
    valor = int("45")
except ValueError:
    print("Error de conversión")
else:
    print(f"Conversión exitosa: {valor}")   # solo si NO hubo excepción
finally:
    print("Esto se ejecuta siempre")           # limpieza, cierre de recursos, etc.
```

```python
# Caso típico: cerrar un fichero pase lo que pase
f = None
try:
    f = open("datos.csv")
    contenido = f.read()
except FileNotFoundError:
    print("Fichero no encontrado")
finally:
    if f:
        f.close()
```
📌 En la práctica, para ficheros se usa `with open(...)` que ya gestiona el cierre automáticamente (ver página de Ficheros).

---

## 🔹 Lanzar excepciones propias (`raise`)

```python
def validar_temperatura(temp):
    if temp < -50 or temp > 200:
        raise ValueError(f"Temperatura fuera de rango: {temp}")
    return temp

try:
    validar_temperatura(500)
except ValueError as e:
    print(e)     # Temperatura fuera de rango: 500

# Re-lanzar una excepción tras capturarla (para loguear y propagar)
try:
    int("abc")
except ValueError:
    print("Logueando el error...")
    raise            # relanza la misma excepción
```

---

## 🔹 Crear excepciones personalizadas

```python
class TemperaturaInvalidaError(Exception):
    """Excepción para valores de temperatura fuera de rango físico."""
    pass

def validar(temp):
    if temp < -273.15:
        raise TemperaturaInvalidaError(f"{temp}°C está por debajo del cero absoluto")
    return temp

try:
    validar(-300)
except TemperaturaInvalidaError as e:
    print(f"Error de dominio: {e}")
```

📌 Muy útil en pipelines de datos: crear excepciones específicas (`DatosCorruptosError`, `EsquemaInvalidoError`) hace el código más legible y permite capturarlas de forma selectiva.

---

## 🔹 Jerarquía de excepciones (básico)

```
BaseException
 └── Exception
      ├── ValueError
      ├── TypeError
      ├── KeyError
      ├── IndexError
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── OSError
      │    └── FileNotFoundError
      └── ... (tus excepciones personalizadas heredan de Exception)
```

```python
# Capturar por la clase padre también captura las hijas
try:
    10 / 0
except ArithmeticError:            # ZeroDivisionError hereda de ArithmeticError
    print("Error aritmético")
```

---

## 🔹 Patrón defensivo típico en Data Engineering

```python
def procesar_fila(fila: dict) -> dict | None:
    try:
        return {
            "id": fila["id"],
            "valor": float(fila["valor"]),
            "fecha": fila["fecha"]
        }
    except KeyError as e:
        print(f"Campo faltante: {e}")
        return None
    except ValueError as e:
        print(f"Valor inválido: {e}")
        return None

filas = [{"id": 1, "valor": "45.6", "fecha": "2026-01-01"},
         {"id": 2, "valor": "abc", "fecha": "2026-01-02"}]

resultados = [r for f in filas if (r := procesar_fila(f)) is not None]
```

---

## 🔹 Errores comunes al usar try/except

```python
# except demasiado genérico oculta bugs reales
try:
    resultado = funcion_compleja()
except:                              # ❌ captura TODO, incluso errores de programación
    pass

# Usar except Exception silenciosamente sin loguear nada
try:
    procesar()
except Exception:
    pass                               # ❌ el error desaparece sin dejar rastro, muy difícil de depurar

# Comprobar tipos con try/except cuando un if hubiera bastado
try:
    if isinstance(x, int):             # innecesariamente complejo
        pass
except:
    pass
```

📌 **Regla práctica (EAFP vs LBYL):** en Python es común el estilo *"Easier to Ask Forgiveness than Permission"* — usar `try/except` en vez de comprobar condiciones antes (`if`). Pero eso no significa capturar excepciones sin más: siempre loguea o gestiona el error, no lo silencies.

---

## 🔹 Tabla resumen ultra-rápida

| Quiero... | Código |
|---|---|
| Capturar error específico | `except ValueError:` |
| Capturar varios tipos | `except (ValueError, TypeError):` |
| Ver el mensaje de error | `except Exception as e: print(e)` |
| Ejecutar solo si NO hubo error | `else:` |
| Ejecutar siempre | `finally:` |
| Lanzar error propio | `raise ValueError("mensaje")` |
| Relanzar el error capturado | `raise` (sin argumentos, dentro del except) |
| Crear excepción personalizada | `class MiError(Exception): pass` |
