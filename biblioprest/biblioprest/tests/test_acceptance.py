"""Un test por criterio de aceptación (docs/acceptance-tests.md)."""
import os
os.environ["DATABASE_URL"] = "sqlite:///./test_biblioprest.db"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

c = TestClient(app)
HOY = "2026-11-13"


@pytest.fixture(autouse=True)
def limpio():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)


def libro(isbn="1", copias=1):
    return c.post("/api/libros", json={"isbn": isbn, "titulo": f"L{isbn}", "autor": "A", "copias_totales": copias}).json()


def socio(tipo="ESTUDIANTE", doc="1"):
    return c.post("/api/socios", json={"nombre": f"S{doc}", "documento": doc, "tipo": tipo}).json()


def prestar(l, s, f=HOY):
    return c.post("/api/prestamos", json={"libro_id": l["id"], "socio_id": s["id"], "fecha": f})


def devolver(p, f=HOY):
    return c.post(f"/api/prestamos/{p['id']}/devolver", json={"fecha": f})


def test_at01_isbn_duplicado():
    libro("9780001")
    r = c.post("/api/libros", json={"isbn": "9780001", "titulo": "X", "autor": "Y", "copias_totales": 1})
    assert r.status_code == 409 and r.json()["detail"] == "El ISBN ya está registrado."


def test_at02_prestamo_exitoso():
    l, s = libro(copias=2), socio()
    r = prestar(l, s)
    assert r.status_code == 201 and r.json()["fecha_vencimiento"] == "2026-11-20"
    assert c.get("/api/libros").json()[0]["copias_disponibles"] == 1


def test_at03_sin_copias():
    l = libro()
    prestar(l, socio(doc="1"))
    r = prestar(l, socio(doc="2"))
    assert r.status_code == 409 and r.json()["detail"] == "No hay copias disponibles."


def test_at04_limite_por_tipo():
    s = socio("EXTERNO")
    for i in range(2):
        assert prestar(libro(str(i)), s).status_code == 201
    r = prestar(libro("9"), s)
    assert r.status_code == 409 and "límite" in r.json()["detail"]


def test_at05_socio_con_vencidos():
    s = socio()
    prestar(libro("1"), s, "2026-11-01")
    r = prestar(libro("2"), s)
    assert r.status_code == 409 and r.json()["detail"] == "El socio tiene préstamos vencidos."


def test_at06_at11_at12_multas():
    s = socio()
    p = prestar(libro("1"), s, "2026-11-03").json()           # vence 2026-11-10
    assert devolver(p).json()["multa"] == 300                 # AT-11: 3 días x $100
    r = prestar(libro("2"), s)                                # AT-06
    assert r.status_code == 409 and r.json()["detail"] == "El socio tiene multas impagas."
    assert c.post(f"/api/socios/{s['id']}/pagos", json={"monto": 100}).json()["saldo_multas"] == 200
    assert c.post(f"/api/socios/{s['id']}/pagos", json={"monto": 500}).status_code == 400   # AT-12


def test_at07_mismo_libro_dos_veces():
    l, s = libro(copias=2), socio()
    prestar(l, s)
    r = prestar(l, s)
    assert r.status_code == 409 and "ya tiene este libro" in r.json()["detail"]


def test_at08_renovacion_valida():
    p = prestar(libro(), socio("DOCENTE"), "2026-11-06").json()   # vence 2026-11-20
    r = c.post(f"/api/prestamos/{p['id']}/renovar", json={"fecha": HOY}).json()
    assert r["fecha_vencimiento"] == "2026-12-04" and r["renovado"] is True


def test_at09_renovacion_rechazada():
    p = prestar(libro("1"), socio("DOCENTE", "1"), "2026-11-06").json()
    c.post(f"/api/prestamos/{p['id']}/renovar", json={"fecha": HOY})
    assert c.post(f"/api/prestamos/{p['id']}/renovar", json={"fecha": HOY}).status_code == 409
    v = prestar(libro("2"), socio("ESTUDIANTE", "2"), "2026-11-01").json()   # ya vencido
    assert c.post(f"/api/prestamos/{v['id']}/renovar", json={"fecha": HOY}).status_code == 409


def test_at10_devolucion_a_tiempo():
    l = libro()
    p = prestar(l, socio(), HOY).json()
    r = devolver(p, "2026-11-19").json()
    assert r["multa"] == 0 and c.get("/api/libros").json()[0]["copias_disponibles"] == 1


def test_at13_baja_libro_prestado():
    l = libro()
    prestar(l, socio())
    assert c.delete(f"/api/libros/{l['id']}").status_code == 409
    assert len(c.get("/api/libros").json()) == 1


def test_at14_baja_socio_con_prestamos():
    s = socio()
    prestar(libro(), s)
    assert c.delete(f"/api/socios/{s['id']}").status_code == 409
