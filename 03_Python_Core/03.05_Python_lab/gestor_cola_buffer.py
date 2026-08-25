# ==============================================================================
# ARCHIVO: gestor_cola_buffer.py
# DESCRIPCIÓN: Sistema interactivo para la gestión y procesamiento de una cola
#              de tareas (buffer) en Python.
# 
# REQUISITOS DEL PROBLEMA:
# 1. Crear una lista inicial con al menos 6 tareas pendientes (strings).
# 2. Implementar un menú interactivo en consola con un bucle continuo (`while True`)
#    que presente las siguientes opciones:
#    - 1. Ver estado actual de la cola (imprimir elementos con sus índices).
#    - 2. Procesar tarea por índice: Eliminar el elemento usando el método `.pop()`
#         y retornar un mensaje indicando la tarea procesada.
#    - 3. Cancelar tarea por índice: Eliminar el elemento de memoria usando `del`
#         confirmando la eliminación sin retornar el valor.
#    - 4. Cancelar un rango de tareas: Solicitar un índice inicial y final para 
#         eliminar un bloque de elementos mediante slicing y la sentencia `del`.
#    - 5. Salir del programa.
# 3. Control de Errores y Excepciones (Obligatorio):
#    - Prevenir o capturar `IndexError` si se ingresa un índice fuera de rango.
#    - Capturar `ValueError` si el usuario introduce texto en vez de números.
#    - Asegurar que la aplicación no colapse ante entradas inválidas y continúe
#      en ejecución hasta seleccionar explícitamente la opción de salir.
# ==============================================================================

cola = [
    "Enviar email", 
    "Generar reporte", 
    "Limpiar BD", 
    "Backup diario", 
    "Actualizar API", 
    "Notificar usuario"
]


def menu():
    while True:
        print('\n-- MENU --')
        print('1. Ver estado de la cola')
        print('2. Procesar tarea por índice (pop)')
        print('3. Cancelar tarea por índice (del)')
        print('4. Cancelar un rango de tareas (del slice)')
        print('5. Salir\n')
        
        try:
            opcion = int(input('Selecciona opción (1-5): '))
        except ValueError:
            print('¡Error! Debes introducir un número entero.')
            continue

        if opcion == 1:
            menu_1(cola)
        elif opcion == 2:
            menu_2()
        elif opcion == 3:
            menu_3()
        elif opcion == 4:
            menu_4()
        elif opcion == 5:
            print('Saliendo del programa...')
            break
        else:
            print('Opción fuera de rango. Elige entre 1 y 5.')


def menu_1(lista_tareas: list):
    print('\n--- ESTADO DE LA COLA ---')
    if not lista_tareas:
        print('(La cola está vacía)')
    else:
        for idx, tarea in enumerate(lista_tareas):
            print(f"[{idx}] {tarea}")


def menu_2():
    try:
        i = int(input('\nSelecciona índice de tarea a procesar: '))
        tarea = cola.pop(i)  # Si el índice no existe, salta directamente a IndexError
        print(f'Se procesó la tarea: "{tarea}"')
    except IndexError:
        print(f'Error: El índice {i} no existe en la cola.')
    except ValueError:
        print('Error: Debes introducir un número entero válido.')


def menu_3():
    try:
        i = int(input('\nSelecciona índice de tarea a eliminar: '))
        if 0 <= i < len(cola):
            del cola[i]
            print('La tarea se eliminó correctamente.')
        else:
            print(f'Error: El índice {i} no está en el rango [0-{len(cola)-1}].')
    except ValueError:
        print('Error: Debes introducir un número entero válido.')


def menu_4():
    try:
        i1 = int(input('\nSelecciona índice de inicio: '))
        i2 = int(input('Selecciona índice final (no incluido): '))
        
        if 0 <= i1 < len(cola) and 0 < i2 <= len(cola) and i1 < i2:
            del cola[i1:i2]
            print(f'Se eliminó el rango del índice {i1} al {i2-1}.')
        else:
            print('Rango incorrecto o fuera de los límites actuales de la cola.')
    except ValueError:
        print('Error: Debes introducir números enteros válidos.')


if __name__ == "__main__":
    menu()