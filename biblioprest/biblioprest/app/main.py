from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .api import router
from .db import Base, engine
from .services import ReglaNegocioError

STATIC = Path(__file__).parent / "static"
Base.metadata.create_all(engine)

app = FastAPI(title="BiblioPrest", description="Gestión de préstamos de biblioteca")


@app.exception_handler(ReglaNegocioError)
def regla_violada(_: Request, e: ReglaNegocioError):
    return JSONResponse({"detail": e.mensaje}, status_code=e.codigo)


app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(STATIC / "index.html")
