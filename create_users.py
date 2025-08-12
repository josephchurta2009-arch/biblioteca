#!/usr/bin/env python3
"""
Script to create initial users for the library management system
"""

from app import app, db
from models import User, Book
from datetime import datetime

def create_initial_data():
    with app.app_context():
        # Eliminar y crear tablas (solo para pruebas o reinicio de base)
        db.drop_all()
        db.create_all()

        # Crear usuarios
        admin = User(
            username="admin",
            email="admin@biblioteca.com",
            first_name="Administrador",
            last_name="Sistema",
            role="admin"
        )
        admin.set_password("admin123")

        student = User(
            username="estudiante",
            email="estudiante@biblioteca.com",
            first_name="Juan",
            last_name="Pérez",
            role="student"
        )
        student.set_password("estudiante123")

        student2 = User(
            username="maria",
            email="maria@biblioteca.com",
            first_name="María",
            last_name="García",
            role="student"
        )
        student2.set_password("maria123")

        db.session.add_all([admin, student, student2])

        # Verificar duplicados por ISBN
        libros = [
            {
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "isbn": "978-84-376-0494-7",
                "publisher": "Editorial Sudamericana",
                "year": 1967,
                "category": "Literatura",
                "desc": "Una de las obras más importantes de la literatura latinoamericana",
                "total": 3
            },
            {
                "title": "Don Quijote de la Mancha",
                "author": "Miguel de Cervantes",
                "isbn": "978-84-376-0495-4",
                "publisher": "Planeta",
                "year": 1605,
                "category": "Clásicos",
                "desc": "La obra cumbre de la literatura española",
                "total": 2
            },
            {
                "title": "Introducción a la Programación",
                "author": "John Smith",
                "isbn": "978-84-376-0496-1",
                "publisher": "Tech Books",
                "year": 2020,
                "category": "Informática",
                "desc": "Guía completa para aprender programación desde cero",
                "total": 5
            },
            {
                "title": "Historia de España",
                "author": "Antonio López",
                "isbn": "978-84-376-0497-8",
                "publisher": "Historia Editorial",
                "year": 2018,
                "category": "Historia",
                "desc": "Recorrido completo por la historia española",
                "total": 2
            },
        ]

        for libro in libros:
            existe = Book.query.filter_by(isbn=libro["isbn"]).first()
            if not existe:
                nuevo = Book(
                    title=libro["title"],
                    author=libro["author"],
                    isbn=libro["isbn"],
                    publisher=libro["publisher"],
                    publication_year=libro["year"],
                    category=libro["category"],
                    description=libro["desc"],
                    total_copies=libro["total"],
                    available_copies=libro["total"],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(nuevo)

        db.session.commit()

        print("✓ Usuarios creados:")
        print("  - admin (admin123) - Administrador")
        print("  - estudiante (estudiante123) - Estudiante")
        print("  - maria (maria123) - Estudiante")
        print()
        print("✓ Libros agregados (si no existían previamente):")
        for libro in libros:
            print(f"  - {libro['title']}")
        print("\n¡Base de datos inicializada correctamente!")

if __name__ == "__main__":
    create_initial_data()
