# Plan técnico

## Stack
- **Backend:** Python 3.11 + FastAPI
- **Base de datos:** SQLite con SQLAlchemy
- **Frontend:** HTML + JavaScript simple (servido por FastAPI)
- **Pruebas:** pytest

## Estructura
```
biblioprest/
├── app/
│   ├── main.py          # arranque y manejo de errores de negocio
│   ├── api.py           # rutas HTTP
│   ├── services.py      # TODAS las reglas RN-xx y políticas por tipo de socio
│   ├── db.py            # modelos (data-model.md) y conexión
│   └── static/          # index.html, logo.svg
├── tests/               # un test por cada AT-xx
├── seed.py              # datos de demo
└── docs/                # esta especificación
```

## Decisiones
1. Las reglas viven en `services.py`; los routers solo traducen HTTP.
2. Los errores de negocio se lanzan como `ReglaNegocioError` y el router los convierte en 409.
3. La fecha "hoy" se inyecta como parámetro para poder probar atrasos.
4. Cada operación de préstamo/devolución corre en una transacción.

## API
| Método | Ruta | Historia |
|---|---|---|
| POST | /libros | HU-01 |
| GET | /libros?q= | HU-08 |
| DELETE | /libros/{id} | RN-11 |
| POST | /socios | HU-02 |
| DELETE | /socios/{id} | RN-12 |
| POST | /prestamos | HU-03 |
| POST | /prestamos/{id}/renovar | HU-04 |
| POST | /prestamos/{id}/devolver | HU-05 |
| GET | /prestamos?estado=activo\|vencido | HU-06 |
| POST | /socios/{id}/pagos | HU-07 |

## Pantallas
1. Libros (lista, búsqueda, alta)
2. Socios (lista, alta, saldo)
3. Préstamos (nuevo, renovar, devolver, vencidos)
