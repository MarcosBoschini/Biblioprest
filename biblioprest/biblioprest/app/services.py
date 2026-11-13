"""Reglas de negocio RN-01 a RN-14 (ver docs/spec.md). Aquí vive TODA la lógica."""
from datetime import date, timedelta
from .db import Libro, Socio, Prestamo

# tipo: (máx. préstamos, días de préstamo, multa por día)
POLITICAS = {"ESTUDIANTE": (3, 7, 100), "DOCENTE": (5, 14, 50), "EXTERNO": (2, 5, 200)}


class ReglaNegocioError(Exception):
    def __init__(self, mensaje: str, codigo: int = 409):
        self.mensaje, self.codigo = mensaje, codigo


def _get(db, modelo, id_):
    obj = db.get(modelo, id_)
    if not obj:
        raise ReglaNegocioError("No encontrado.", 404)
    return obj


def _activos(db, **filtro):
    return db.query(Prestamo).filter_by(fecha_devolucion=None, **filtro).all()


def crear_libro(db, isbn, titulo, autor, copias):
    if db.query(Libro).filter_by(isbn=isbn).first():                       # RN-01
        raise ReglaNegocioError("El ISBN ya está registrado.")
    libro = Libro(isbn=isbn, titulo=titulo, autor=autor, copias_totales=copias, copias_disponibles=copias)
    db.add(libro); db.commit()
    return libro


def actualizar_copias(db, libro_id, nuevo_total):
    libro = _get(db, Libro, libro_id)
    prestadas = libro.copias_totales - libro.copias_disponibles
    if nuevo_total < prestadas:                                            # RN-11
        raise ReglaNegocioError("No se pueden reducir las copias por debajo de las prestadas.")
    libro.copias_totales, libro.copias_disponibles = nuevo_total, nuevo_total - prestadas
    db.commit()
    return libro


def eliminar_libro(db, libro_id):
    libro = _get(db, Libro, libro_id)
    if _activos(db, libro_id=libro.id):                                    # RN-11
        raise ReglaNegocioError("El libro tiene préstamos activos.")
    db.query(Prestamo).filter_by(libro_id=libro.id).delete()
    db.delete(libro); db.commit()


def crear_socio(db, nombre, documento, tipo):
    if db.query(Socio).filter_by(documento=documento).first():
        raise ReglaNegocioError("El documento ya está registrado.")
    socio = Socio(nombre=nombre, documento=documento, tipo=tipo)
    db.add(socio); db.commit()
    return socio


def baja_socio(db, socio_id):
    socio = _get(db, Socio, socio_id)
    if _activos(db, socio_id=socio.id) or socio.saldo_multas > 0:          # RN-12
        raise ReglaNegocioError("El socio tiene préstamos activos o multas impagas.")
    socio.activo = False; db.commit()
    return socio


def prestar(db, libro_id, socio_id, fecha=None):
    hoy = fecha or date.today()
    libro, socio = _get(db, Libro, libro_id), _get(db, Socio, socio_id)
    if not socio.activo:                                                   # RN-14
        raise ReglaNegocioError("El socio está dado de baja.")
    activos = _activos(db, socio_id=socio.id)
    if any(p.fecha_vencimiento < hoy for p in activos):                    # RN-04
        raise ReglaNegocioError("El socio tiene préstamos vencidos.")
    if socio.saldo_multas > 0:                                             # RN-05
        raise ReglaNegocioError("El socio tiene multas impagas.")
    maximo, dias, _ = POLITICAS[socio.tipo]
    if len(activos) >= maximo:                                             # RN-03
        raise ReglaNegocioError("El socio alcanzó su límite de préstamos.")
    if any(p.libro_id == libro.id for p in activos):                       # RN-06
        raise ReglaNegocioError("El socio ya tiene este libro en préstamo.")
    if libro.copias_disponibles < 1:                                       # RN-02
        raise ReglaNegocioError("No hay copias disponibles.")
    prestamo = Prestamo(libro_id=libro.id, socio_id=socio.id, fecha_prestamo=hoy,
                        fecha_vencimiento=hoy + timedelta(days=dias))      # RN-07
    libro.copias_disponibles -= 1
    db.add(prestamo); db.commit()
    return prestamo


def renovar(db, prestamo_id, fecha=None):
    hoy = fecha or date.today()
    p = _get(db, Prestamo, prestamo_id)
    if p.fecha_devolucion or p.renovado or p.fecha_vencimiento < hoy:      # RN-08, RN-09
        raise ReglaNegocioError("El préstamo no puede renovarse.")
    p.fecha_vencimiento += timedelta(days=POLITICAS[p.socio.tipo][1])
    p.renovado = True; db.commit()
    return p


def devolver(db, prestamo_id, fecha=None):
    hoy = fecha or date.today()
    p = _get(db, Prestamo, prestamo_id)
    if p.fecha_devolucion:
        raise ReglaNegocioError("El préstamo ya fue devuelto.")
    atraso = max(0, (hoy - p.fecha_vencimiento).days)
    p.multa = atraso * POLITICAS[p.socio.tipo][2]                          # RN-10
    p.socio.saldo_multas += p.multa
    p.libro.copias_disponibles += 1                                        # RN-02
    p.fecha_devolucion = hoy; db.commit()
    return p


def pagar(db, socio_id, monto):
    socio = _get(db, Socio, socio_id)
    if monto <= 0:
        raise ReglaNegocioError("El pago debe ser mayor a 0.", 400)
    if monto > socio.saldo_multas:                                         # RN-13
        raise ReglaNegocioError("El pago supera el saldo.", 400)
    socio.saldo_multas -= monto; db.commit()
    return socio


def listar_prestamos(db, estado=None, hoy=None):
    hoy = hoy or date.today()
    q = db.query(Prestamo).order_by(Prestamo.id.desc())
    if estado in ("activo", "vencido"):
        q = q.filter(Prestamo.fecha_devolucion.is_(None))
    items = q.all()
    if estado == "vencido":
        items = [p for p in items if p.fecha_vencimiento < hoy]
    return items
