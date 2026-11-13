"""Base de datos y modelos (ver docs/data-model.md)."""
import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import date

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./biblioprest.db"),
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Libro(Base):
    __tablename__ = "libros"
    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(unique=True)
    titulo: Mapped[str]
    autor: Mapped[str]
    copias_totales: Mapped[int]
    copias_disponibles: Mapped[int]


class Socio(Base):
    __tablename__ = "socios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    documento: Mapped[str] = mapped_column(unique=True)
    tipo: Mapped[str]
    saldo_multas: Mapped[int] = mapped_column(default=0)
    activo: Mapped[bool] = mapped_column(default=True)


class Prestamo(Base):
    __tablename__ = "prestamos"
    id: Mapped[int] = mapped_column(primary_key=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"))
    socio_id: Mapped[int] = mapped_column(ForeignKey("socios.id"))
    fecha_prestamo: Mapped[date]
    fecha_vencimiento: Mapped[date]
    fecha_devolucion: Mapped[date | None] = mapped_column(default=None)
    renovado: Mapped[bool] = mapped_column(default=False)
    multa: Mapped[int] = mapped_column(default=0)
    libro: Mapped[Libro] = relationship()
    socio: Mapped[Socio] = relationship()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
