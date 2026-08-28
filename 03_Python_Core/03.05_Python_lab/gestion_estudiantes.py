# ==============================================================================
# Sistema de Gestión de Registros Estudiantiles
# 
# Diseña un programa en Python para gestionar información de estudiantes utilizando
# estructuras de datos integradas (diccionarios, conjuntos y listas). El sistema 
# debe permitir:
# 1. Registrar nuevos estudiantes con su edad y una lista inicial de cursos.
# 2. Asignar calificaciones numéricas a estudiantes existentes.
# 3. Verificar si un estudiante está matriculado en un curso específico.
# 4. Calcular el promedio de calificaciones de un estudiante.
# 5. Filtrar y retornar una lista con los nombres de aquellos estudiantes cuyo 
#    promedio de calificaciones supere un umbral (threshold) determinado.
# ==============================================================================

student_records = {}

def add_student(name: str, age: int, courses: list):
    if name in student_records:
        print(f"Student '{name}' already exists.")
    else:
        student_records[name] = {'age': age, 'grades': set(), 'courses': set(courses)}
        print(f"Student '{name}' added successfully.")

def add_grade(name: str, grade: int):
    if name in student_records:
        student_records[name]['grades'].add(grade)
        print(f"Grade {grade} added for student '{name}'.")
    else:
        print(f"Student '{name}' not found.")

def is_enrolled(name: str, course: str): 
    if name in student_records:
        return course in student_records[name]['courses']
    else:
        print(f"Student '{name}' not found.")
        return False

def calculate_average_grade(name: str):
    if name not in student_records:
        print(f"Student '{name}' not found.")
        return None
    
    grades = student_records[name]['grades']
    if not grades:
        return 0.0
    
    return sum(grades) / len(grades)

def filter_top_students(threshold: float):
    student_list = []
    for name in student_records.keys():
        avg_student = calculate_average_grade(name)
        if avg_student is not None and avg_student > threshold:
            student_list.append(name)
    return student_list

# --- Casos de Prueba ---
add_student("Alice", 20, ["Math", "Physics"])
add_student("Bob", 22, ["Math", "Biology"])
add_student("Diana", 23, ["Chemistry", "Physics"])

add_grade("Alice", 90)
add_grade("Alice", 85)
add_grade("Bob", 75)
add_grade("Diana", 95)

print(filter_top_students(80))   
print(filter_top_students(90))   
print(filter_top_students(100))  