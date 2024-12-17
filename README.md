# M7-L1-AccesoADatos_16-12-2024

# Proyecto Django: Sistema de Gestión Escolar

## Descripción General
Este es un proyecto basado en Django para gestionar estudiantes y cursos en una escuela. Incluye modelos, vistas, plantillas y consultas SQL personalizadas para manejar los datos de manera eficiente.

---

## Requisitos Previos
- Python 3.8+
- Django 4.x
- Base de datos PostgreSQL
- pip (Administrador de paquetes de Python)

---

## Instrucciones de Configuración

### 1. Clonar el Repositorio
```bash
$ git clone <repository-url>
$ cd <repository-folder>
```

### 2. Crear un Entorno Virtual
```bash
$ python -m venv venv
$ source venv/bin/activate  # En Windows, usar `venv\Scripts\activate`
```

### 3. Instalar Dependencias
```bash
$ pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
Actualizar la sección `DATABASES` en el archivo `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'School_DB',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Asegúrese de que PostgreSQL esté instalado y ejecutándose. Cree la base de datos manualmente:
```bash
$ psql -U postgres
postgres=# CREATE DATABASE School_DB;
```

### 5. Aplicar Migraciones
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### 6. Crear un Superusuario
```bash
$ python manage.py createsuperuser
```
Siga las instrucciones para crear una cuenta de administrador.

### 7. Ejecutar el Servidor de Desarrollo
```bash
$ python manage.py runserver
```
Acceda a la aplicación en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Estructura de la Aplicación

### Modelos
- **Student**: Almacena información básica sobre los estudiantes, como nombre, apellido, correo electrónico, edad y fecha de inscripción.
- **Course**: Contiene detalles del curso, como nombre, descripción y una relación de muchos a muchos con los estudiantes.

### Vistas
- **custom_sql_query**: Ejecuta una consulta SQL personalizada para obtener estudiantes mayores de 18 años.
- **raw_query_example**: Utiliza el método `raw()` de Django para obtener estudiantes menores de 18 años.

### Plantillas
- **students.html**: Muestra una lista de estudiantes basada en los resultados de las consultas.

### URLs
- `/admin/`: Panel de administración.
- `/custom-query/`: Endpoint para la vista `custom_sql_query`.
- `/raw-query/`: Endpoint para la vista `raw_query_example`.

---

## Archivos

### `models.py`
```python
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    enrollment_date = models.DateField(auto_now_add=True)

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    students = models.ManyToManyField(Student, related_name='courses')

    def __str__(self):
        return self.name
```

### `views.py`
```python
from django.shortcuts import render
from django.db import connection  
from .models import Student

def custom_sql_query(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM school_student WHERE age > %s", [18])
        rows = cursor.fetchall()

    return render(request, 'students.html', {'students': rows})

def raw_query_example(request):
    students = Student.objects.raw('SELECT * FROM school_student WHERE age < %s', [18])
    return render(request, 'students.html', {'students': students})
```

### `students.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Students</title>
</head>
<body>
    <h1>Lista de Estudiantes</h1>
    <ul>
        {% for student in students %}
            <li>{{ student }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### `urls.py`
```python
from django.contrib import admin
from django.urls import path
from school import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-query/', views.custom_sql_query, name='custom_query'),
    path('raw-query/', views.raw_query_example, name='raw_query'),
]
```

### `settings.py`
Secciones relevantes:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'school',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'School_DB',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Pruebas

### Acceder al Panel de Administración
1. Vaya a [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
2. Inicie sesión con las credenciales del superusuario.
3. Agregue estudiantes y cursos a través de la interfaz de administración.

### Probar Endpoints
- **Consulta SQL Personalizada**: Visite [http://127.0.0.1:8000/custom-query/](http://127.0.0.1:8000/custom-query/).
- **Ejemplo de Consulta Raw**: Visite [http://127.0.0.1:8000/raw-query/](http://127.0.0.1:8000/raw-query/).

---

## Notas
- Utilice la interfaz de administración de Django para gestionar los datos de estudiantes y cursos.
- Las consultas en `views.py` demuestran el uso de SQL en bruto en Django; asegúrese de sanitizar adecuadamente para prevenir inyecciones SQL en entornos de producción.

---

## Mejoras Futuras
- Agregar autenticación de usuarios para un acceso seguro.
- Mejorar el diseño de la plantilla `students.html` utilizando CSS o un framework frontend como Bootstrap.
- Implementar endpoints de API para operaciones CRUD utilizando Django REST Framework.

