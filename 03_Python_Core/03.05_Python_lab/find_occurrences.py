"""
Enunciado:
Crea una función llamada find_occurrences que:
- Tome dos argumentos de cadena: text y pattern.
- Cuente cuántas veces aparece pattern en text, incluyendo ocurrencias superpuestas.
- Devuelva una tupla que contenga:
    1. Un booleano que indique si se encontró el patrón (True/False).
    2. El número de ocurrencias del patrón.
    3. Una lista de las posiciones iniciales (índices) donde se encontró el patrón.

Ejemplo:
    text = "abababab", pattern = "aba"
    Retorna: (True, 3, [0, 2, 4])

    Si no se encuentra el patrón o las entradas no son válidas:
    Retorna: (False, 0, [])
"""


def find_occurrences(text: str, pattern: str) -> tuple[bool, int, list[int]]:
    if not pattern or not text:
        return False, 0, []

    positions = []
    pattern_len = len(pattern)

    # Recorremos el texto evaluando cada subcadena con superposición
    for i in range(len(text) - pattern_len + 1):
        if text[i : i + pattern_len] == pattern:
            positions.append(i)

    count = len(positions)
    found = count > 0

    return found, count, positions


# Pruebas para verificar el funcionamiento
if __name__ == "__main__":
    print(find_occurrences("abababab", "aba"))  # (True, 3, [0, 2, 4])
    print(find_occurrences("hello world", "xyz"))  # (False, 0, [])