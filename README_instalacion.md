# Sistema de Biblioteca Digital - Instalación Local

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install Flask==3.1.1
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Login==0.6.3
pip install Flask-Dance==7.1.0
pip install SQLAlchemy==2.0.41
pip install Werkzeug==3.1.3
pip install email-validator==2.2.0
pip install psycopg2-binary==2.9.10
pip install oauthlib==3.2.2
pip install PyJWT==2.10.1
pip install gunicorn==23.0.0
```

### 3. Configurar variables de entorno
```bash
# En Windows:
set SESSION_SECRET=tu_clave_secreta_aqui
set FLASK_ENV=development

# En Linux/Mac:
export SESSION_SECRET=tu_clave_secreta_aqui
export FLASK_ENV=development
```

### 4. Inicializar la base de datos
```bash
python create_users.py
```

### 5. Ejecutar la aplicación
```bash
python main.py
```

La aplicación estará disponible en: http://localhost:5000

## Usuarios de Prueba

### Administrador
- Usuario: `admin`
- Contraseña: `admin123`

### Estudiantes
- Usuario: `estudiante` / Contraseña: `estudiante123`
- Usuario: `maria` / Contraseña: `maria123`

## Funcionalidades

### Como Administrador:
- Gestionar libros (agregar, editar, eliminar)
- Ver todos los préstamos
- Gestionar usuarios
- Estadísticas del sistema

### Como Estudiante:
- Buscar libros por título, autor o categoría
- Solicitar préstamos
- Ver mis préstamos activos
- Devolver libros

## Estructura del Proyecto

```
biblioteca-digital/
├── app.py              # Configuración principal de Flask
├── main.py             # Punto de entrada de la aplicación
├── models.py           # Modelos de base de datos
├── routes.py           # Rutas y lógica de la aplicación
├── replit_auth.py      # Autenticación (opcional para Replit)
├── create_users.py     # Script para crear usuarios iniciales
├── static/
│   ├── css/           # Estilos CSS
│   └── js/            # JavaScript
├── templates/         # Plantillas HTML
├── library.db         # Base de datos SQLite
└── README_instalacion.md
```

## Notas Importantes

1. **Base de datos**: El sistema usa SQLite por defecto, que es ideal para desarrollo y pruebas.
2. **Autenticación**: Para uso local, se usa autenticación básica con usuario/contraseña.
3. **Archivos estáticos**: CSS y JavaScript están en las carpetas `static/css` y `static/js`.
4. **Plantillas**: Las vistas HTML están en la carpeta `templates`.

## Solución de Problemas

### Error de importación:
```bash
# Asegúrate de estar en el directorio correcto
cd biblioteca-digital
python main.py
```

### Error de base de datos:
```bash
# Elimina la base de datos y recréala
rm library.db
python create_users.py
```

### Error de dependencias:
```bash
# Reinstala las dependencias
pip install --force-reinstall Flask Flask-SQLAlchemy Flask-Login
```

## Personalización

- **Estilos**: Edita los archivos en `static/css/`
- **Plantillas**: Modifica los archivos HTML en `templates/`
- **Lógica**: Ajusta las rutas en `routes.py`
- **Modelos**: Modifica la estructura de datos en `models.py`

¡Disfruta usando el Sistema de Biblioteca Digital!