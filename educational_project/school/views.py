from django.shortcuts import render
from django.db import connection  
from .models import Student

# Diccionario: Consulta directa a la base de datos
def custom_sql_query(request):
    with connection.cursor() as cursor:
        #            nombre de la aplicacion_nombre de tabla
        cursor.execute("SELECT * FROM school_student WHERE age >= %s", [20])
        rows = cursor.fetchall()

    return render(request, 'students.html', {'students': rows})

# Lista indice - columnas / toma como intermediario el modelo.
def raw_query_example(request):
    # Visualiza en Objetos:
    students = Student.objects.raw('SELECT * FROM school_student WHERE age < %s', [20])

    return render(request, 'students.html', {'students': students})














    # Convierte el QuerySet en una lista de diccionarios para pasar información específica a la plantilla
    # student_data = [
    #     # {'0': student.id,
    #     #  '1': student.first_name, 
    #     #  '2': student.last_name, 
    #     #  '3': student.email, 
    #     #  '4': student.age,
    #     #  '5': student.enrollment_date
    #     #  } 

    #     {'id': student.id,
    #      'first_name': student.first_name, 
    #      'last_name': student.last_name, 
    #      'email': student.email, 
    #      'age': student.age,
    #      'enrollment_date': student.enrollment_date
    #      } 
    #     for student in students
    # ]