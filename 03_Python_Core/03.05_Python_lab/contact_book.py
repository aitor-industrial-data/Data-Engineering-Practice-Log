"""
===============================================================================
ENUNCIADO DEL PROBLEMA: SISTEMA DE GESTIÓN DE AGENDA DE CONTACTOS (CONTACT BOOK)
===============================================================================

Escribe un programa en Python para gestionar una agenda de contactos interactiva 
utilizando un diccionario (`contact_book`). Cada contacto estará identificado por 
su nombre (clave) y contendrá un diccionario anidado con la información de 'phone', 
'email' y 'address'.

El programa debe implementar el siguiente menú dinámico:
    1. Add Contact: Añade un contacto nuevo si el nombre no existe.
    2. View Contact: Muestra los datos de un contacto por su nombre.
    3. Edit Contact: Actualiza la información de un contacto existente.
    4. Delete Contact: Elimina un contacto de la agenda.
    5. List All Contacts: Muestra todos los contactos registrados o "No contacts available."
    6. Exit: Finaliza la ejecución del programa.

REQUISITOS Y VALIDACIONES:
- Las entradas del usuario para el menú y los datos de contacto se leen vía `input()`.
- Si se introduce una opción fuera del rango válido (1-5 para acciones, 6 salir), 
  se debe imprimir el mensaje: "Invalid choice. Please try again."
- Si un contacto ya existe al añadir, o no existe al consultar/editar/eliminar, 
  se debe emitir el mensaje correspondiente.
"""

def display_menu():
    print('Contact Book Menu:')
    print('1. Add Contact')
    print('2. View Contact')
    print('3. Edit Contact')
    print('4. Delete Contact')
    print('5. List All Contacts')
    print('6. Exit')

def add_contact(contact_book: dict):
    name = input()
    phone = input()
    email = input()
    address = input()

    if name in contact_book:
        print("Contact already exists!")
    else:
        contact_book[name] = {}
        contact_book[name]['phone'] = phone
        contact_book[name]['email'] = email
        contact_book[name]['address'] = address
        print("Contact added successfully!")

def view_contact(contact_book: dict):
    user = input()
    if user in contact_book:
        print(f'Name: {user}')
        print(f"Phone: {contact_book[user]['phone']}")
        print(f"Email: {contact_book[user]['email']}")
        print(f"Address: {contact_book[user]['address']}")
    else:
        print('Contact not found!')

def edit_contact(contact_book: dict):
    name = input()
    if name in contact_book:
        phone = input()
        email = input()
        address = input()
        contact_book[name]['phone'] = phone
        contact_book[name]['email'] = email
        contact_book[name]['address'] = address
        print("Contact updated successfully!")
    else:
        print('Contact not found!')

def delete_contact(contact_book: dict):
    name = input()
    if name in contact_book:
        contact_book.pop(name)
        print("Contact deleted successfully!")
    else:
        print("Contact not found!")

def list_all_contacts(contact_book: dict):
    if contact_book == {}:
        print("No contacts available.")
    else:
        for name in contact_book:
            print(f"Name: {name}")
            print(f"Phone: {contact_book[name]['phone']}")
            print(f"Email: {contact_book[name]['email']}")
            print(f"Address: {contact_book[name]['address']}\n")

# ===============================================================================
# BLOQUE DE PRUEBAS AUTOMATIZADAS (MOCKING DE INPUT/OUTPUT)
# ===============================================================================

if __name__ == '__main__':
    import io
    import sys

    def run_test(simulated_inputs, expected_snippet):
        """Simula entradas de usuario y captura la salida por consola."""
        # Redirigir stdin y stdout
        sys.stdin = io.StringIO("\n".join(simulated_inputs))
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Ejecución del bucle principal
        contact_book = {}
        display_menu()
        menu = int(input())

        while menu != 6:
            if menu not in range(1, 6):
                print("Invalid choice. Please try again.")
            elif menu == 1:
                add_contact(contact_book)
            elif menu == 2:
                view_contact(contact_book)
            elif menu == 3:
                edit_contact(contact_book)
            elif menu == 4:
                delete_contact(contact_book)
            elif menu == 5:
                list_all_contacts(contact_book)
            display_menu()
            menu = int(input())

        # Restaurar stdin/stdout estándar
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        assert expected_snippet in output, f"Test fallido. Esperado conteniendo: '{expected_snippet}'"
        print("✅ Prueba superada con éxito.")

    print("Ejecutando pruebas de integración...")

    # Prueba 1: Opción inválida (0) y luego Salir (6)
    run_test(["0", "6"], "Invalid choice. Please try again.")

    # Prueba 2: Listar agenda vacía (5) y Salir (6)
    run_test(["5", "6"], "No contacts available.")

    # Prueba 3: Añadir un contacto (1) y listar (5)
    run_test(["1", "Aitor", "600112233", "aitor@email.com", "Calle Mayor 1", "5", "6"], "Name: Aitor")

    # Prueba 4: Intentar añadir duplicado
    run_test([
        "1", "Aitor", "600112233", "aitor@email.com", "Calle Mayor 1",
        "1", "Aitor", "600112233", "aitor@email.com", "Calle Mayor 1",
        "6"
    ], "Contact already exists!")

    # Prueba 5: Eliminar contacto (4) y verificar agenda vacía
    run_test([
        "1", "Aitor", "600112233", "aitor@email.com", "Calle Mayor 1",
        "4", "Aitor",
        "5",
        "6"
    ], "No contacts available.")