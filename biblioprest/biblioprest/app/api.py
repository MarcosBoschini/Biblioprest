"""Rutas HTTP: solo traducen entrada/salida; las reglas están en services.py."""
from datetime import date
from typing import Literal, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import services as s
from .db import get_db, Libro, Socio

router = APIRouter()


def d(o):
    return {c.name: (v.isoformat() if isinstance(v := getattr(o, c.name), date) else v)
            for c in o.__table__.columns}


def pd(p, hoy=None):
    hoy = hoy or date.today()
    return {**d(p), "libro": p.libro.titulo, "socio": p.socio.nombre, "tipo": p.socio.tipo,
            "vencido": p.fecha_devolucion is None and p.fecha_vencimiento < hoy}


class LibroIn(BaseModel):
    isbn: str = Field(min_length=1)
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    copias_totales: int = Field(ge=1)


class CopiasIn(BaseModel):
    copias_totales: int = Field(ge=1)


class SocioIn(BaseModel):
    nombre: str = Field(min_length=1)
    documento: str = Field(min_length=1)
    tipo: Literal["ESTUDIANTE", "DOCENTE", "EXTERNO"]


class PrestamoIn(BaseModel):
    libro_id: int
    socio_id: int
    fecha: Optional[date] = None


class FechaIn(BaseModel):
    fecha: Optional[date] = None


class PagoIn(BaseModel):
    monto: int


@router.post("/libros", status_code=201)
def crear_libro(b: LibroIn, db: Session = Depends(get_db)):
    return d(s.crear_libro(db, b.isbn, b.titulo, b.autor, b.copias_totales))


@router.get("/libros")
def buscar_libros(q: str = "", db: Session = Depends(get_db)):
    f = Libro.titulo.ilike(f"%{q}%"), Libro.autor.ilike(f"%{q}%"), Libro.isbn.ilike(f"%{q}%")
    return [d(x) for x in db.query(Libro).filter(or_(*f)).order_by(Libro.titulo).all()]


@router.patch("/libros/{id}")
def copias(id: int, b: CopiasIn, db: Session = Depends(get_db)):
    return d(s.actualizar_copias(db, id, b.copias_totales))


@router.delete("/libros/{id}")
def eliminar_libro(id: int, db: Session = Depends(get_db)):
    s.eliminar_libro(db, id)
    return {"ok": True}


@router.post("/socios", status_code=201)
def crear_socio(b: SocioIn, db: Session = Depends(get_db)):
    return d(s.crear_socio(db, b.nombre, b.documento, b.tipo))


@router.get("/socios")
def listar_socios(db: Session = Depends(get_db)):
    return [d(x) for x in db.query(Socio).order_by(Socio.nombre).all()]


@router.delete("/socios/{id}")
def baja_socio(id: int, db: Session = Depends(get_db)):
    return d(s.baja_socio(db, id))


@router.post("/socios/{id}/pagos")
def pagar(id: int, b: PagoIn, db: Session = Depends(get_db)):
    return d(s.pagar(db, id, b.monto))


@router.post("/prestamos", status_code=201)
def prestar(b: PrestamoIn, db: Session = Depends(get_db)):
    return pd(s.prestar(db, b.libro_id, b.socio_id, b.fecha), b.fecha)


@router.get("/prestamos")
def listar(estado: Optional[str] = None, hoy: Optional[date] = None, db: Session = Depends(get_db)):
    return [pd(p, hoy) for p in s.listar_prestamos(db, estado, hoy)]


@router.post("/prestamos/{id}/renovar")
def renovar(id: int, b: FechaIn = FechaIn(), db: Session = Depends(get_db)):
    return pd(s.renovar(db, id, b.fecha), b.fecha)


@router.post("/prestamos/{id}/devolver")
def devolver(id: int, b: FechaIn = FechaIn(), db: Session = Depends(get_db)):
    return pd(s.devolver(db, id, b.fecha), b.fecha)
