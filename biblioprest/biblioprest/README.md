<p align="center"><img src="app/static/logo.svg" alt="Logo BiblioPrest" width="120"></p>

# BiblioPrest 📚
Gestión de préstamos de biblioteca con reglas de negocio reales, construida con **Spec-Driven Development (SDD)**: primero la especificación (`docs/`), después el código.

## Ejecutar
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py                     # opcional: datos de demo
uvicorn app.main:app --reload
```
Abrir **http://localhost:8000** (interfaz) o **http://localhost:8000/docs** (API interactiva).

## Pruebas
```bash
pytest -v
```
Hay un test por cada criterio de `docs/acceptance-tests.md`.

## Guion de demo (con `python seed.py`)
1. **Socios**: Ana (estudiante) tiene un préstamo vencido. En **Préstamos → Vencidos** aparece en rojo.
2. Intentar prestarle otro libro a Ana → bloqueado por préstamos vencidos (RN-04).
3. **Devolver** el préstamo de Ana → se calcula la multa (3 días × $100 = $300) y queda en su saldo.
4. Intentar prestarle de nuevo → bloqueado por multa impaga (RN-05). En **Socios → Registrar pago**, cancelar la multa.
5. Prestar *Ficciones* (1 sola copia) a Luis y luego a Marta → "No hay copias disponibles" (RN-02).
6. **Renovar** el préstamo de Luis (docente): suma 14 días; una segunda renovación se rechaza (RN-08/09).
7. Cambiar la **fecha simulada** (arriba a la derecha) para mostrar atrasos sin esperar días reales.

## Estructura
```
biblioprest/
├── README.md
├── requirements.txt
├── .gitignore
├── seed.py                  # datos de demo
├── app/
│   ├── main.py              # arranque FastAPI y manejo de errores
│   ├── api.py               # rutas HTTP (/api/...)
│   ├── services.py          # reglas de negocio RN-01..RN-14
│   ├── db.py                # modelos y conexión SQLite
│   └── static/              # index.html y logo.svg
├── tests/
│   └── test_acceptance.py   # criterios de aceptación AT-xx
└── docs/                    # especificación SDD
    ├── constitution.md
    ├── spec.md
    ├── acceptance-tests.md
    ├── data-model.md
    ├── plan.md
    ├── tasks.md
    └── ai-prompts.md
```

## Subir a GitHub
```bash
git init
git add .
git commit -m "BiblioPrest: especificación SDD y aplicación"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/biblioprest.git
git push -u origin main
```
(Crear antes el repositorio vacío en github.com, sin README.)
