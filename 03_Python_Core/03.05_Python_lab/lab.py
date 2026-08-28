student_records={}
def add_student(name:str,age:int,courses:list):
    if name in student_records:
        print(f"Student '{name}' already exists.")
    else:
        student_records[name]={'age':age,'grades':set(),'courses':set(courses)}
        print(f"Student '{name}' added successfully.")



def add_grade(name:str, grade:int):
    if name in student_records:
        student_records[name]['grades'].add(grade)
        print(f"Grade {grade} added for student '{name}'.")
    else:
        print(f"Student '{name}' not found.")


def is_enrolled(name:str, course:str): 
    if name in student_records:
        if course in student_records[name]['courses']:
            return True
        else:
            return False
    else:
        print(f"Student '{name}' not found.")
        return False


def calculate_average_grade(name:str):
    if name not in student_records:
        print(f"Student '{name}' not found.")
        return None
    else:
        
        if student_records[name]['grades']=={}:
            return 0
        else:
            count=0
            suma=0
            for grade in student_records[name]['grades']:
                count+=1
                suma+=grade
            return suma/count
        
def list_students_by_course(course:str):
    student_list=[]
    for name in student_records.keys():
        if course in student_records[name]['courses']:
            student_list.append(name)
    return student_list

def filter_top_students(threshold:float):
    student_list=[]
    for name in student_records.keys():
        avg_student=calculate_average_grade(name)
        if avg_student > threshold:
            student_list.append(name)
    return student_list


add_student("Alice", 20, ["Math", "Physics"])
add_student("Bob", 22, ["Math", "Biology"])
add_student("Diana", 23, ["Chemistry", "Physics"])
add_grade("Alice", 90)
add_grade("Alice", 85)
add_grade("Bob", 75)
add_grade("Diana", 95)
print(filter_top_students(80))  # Debería devolver ["Alice", "Diana"]
print(filter_top_students(90))  # Debería devolver ["Diana"]
print(filter_top_students(100))  # Debería devolver una lista vacía