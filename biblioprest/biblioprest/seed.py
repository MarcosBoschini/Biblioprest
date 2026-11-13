"""Carga datos de demo. Uso: python seed.py  (reinicia la base de datos)."""
from datetime import date, timedelta
from app.db import Base, engine, SessionLocal
from app import services as s

Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
db = SessionLocal()
hoy = date.today()
libros = [s.crear_libro(db, *x) for x in [
    ("978-950-07-0001", "Rayuela", "Julio Cortázar", 2),
    ("978-950-07-0002", "Ficciones", "Jorge Luis Borges", 1),
    ("978-950-07-0003", "El túnel", "Ernesto Sabato", 3),
    ("978-950-07-0004", "Martín Fierro", "José Hernández", 2)]]
ana = s.crear_socio(db, "Ana Gómez", "30111222", "ESTUDIANTE")
luis = s.crear_socio(db, "Luis Pérez", "28333444", "DOCENTE")
s.crear_socio(db, "Marta Ruiz", "20555666", "EXTERNO")
# Préstamo ya vencido (hace 10 días, vence hace 3): sirve para mostrar atraso y multa
s.prestar(db, libros[0].id, ana.id, hoy - timedelta(days=10))
s.prestar(db, libros[2].id, luis.id, hoy - timedelta(days=2))
print("Datos de demo cargados.")
