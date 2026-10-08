# CarRental

Car rental web app: a **FastAPI** backend (SQLite via SQLAlchemy) and a **React** frontend (Vite).

## Project structure

```
backend/
  app/
    main.py          # FastAPI app, CORS, startup (creates tables + seeds sample cars)
    database.py      # SQLAlchemy engine/session
    models.py        # Car, Booking
    schemas.py       # Pydantic request/response models
    seed.py          # Sample data
    routers/         # cars.py, bookings.py
  tests/             # pytest API tests
frontend/
  src/
    api.js           # fetch wrapper for the API
    App.jsx          # routes + navbar
    components/      # CarList, BookingForm, BookingList
```

## Getting started

### Backend (Python 3.10+)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs on http://localhost:8000. Interactive docs: http://localhost:8000/docs

Run the tests (from the repo root):

```bash
make install   # runtime + dev deps (pytest-bdd, ruff)
make test      # all implemented requirements + unit tests
make check     # lint + tests, run before every commit
```

### Frontend (Node 16+)

```bash
cd frontend
nvm use          # picks Node 16 from .nvmrc
npm install
npm run dev
```

App runs on http://localhost:5173. Requests to `/api` are proxied to the backend.

## API overview

| Method | Path                  | Description                         |
|--------|-----------------------|-------------------------------------|
| GET    | `/api/health`         | Health check                        |
| GET    | `/api/cars`           | List cars (`?available=true` filter)|
| GET    | `/api/cars/{id}`      | Get a car                           |
| POST   | `/api/cars`           | Create a car                        |
| PATCH  | `/api/cars/{id}`      | Update a car                        |
| DELETE | `/api/cars/{id}`      | Delete a car                        |
| GET    | `/api/bookings`       | List bookings                       |
| POST   | `/api/bookings`       | Book a car (price computed, overlaps rejected) |
| DELETE | `/api/bookings/{id}`  | Cancel a booking                    |

## Requirements as code

Requirements are executable Gherkin scenarios in `backend/tests/features/`, each tagged with a unique ID:

| File | Covers |
|---|---|
| `cars.feature` | `REQ-SYS-001`, `REQ-CAR-001` … `REQ-CAR-007` |
| `bookings.feature` | `REQ-BKG-001` … `REQ-BKG-009` |
| `backlog.feature` | `REQ-BKG-010` … `REQ-BKG-012`, agreed but **not implemented yet** |

```bash
make req ID=REQ-BKG-001   # run one requirement
make test-backlog         # include backlog (these fail until implemented)
```

## Working with Claude Code

- `CLAUDE.md`: project context, commands, domain rules and gotchas, loaded automatically.
- `.claude/skills/`: `implement-requirement` (spec-first workflow), `backend-standards`,
  `testing-standards`, `frontend-standards`.
- `.claude/settings.json`: lets Claude run `make test`, `make check`, `pytest` and `ruff` without prompting.

Try: *"Implement REQ-BKG-010"* or *"Implement the whole backlog, one requirement at a time."*

## Configuration

| Variable       | Default                    |
|----------------|----------------------------|
| `DATABASE_URL` | `sqlite:///./carrental.db` |
| `CORS_ORIGINS` | `http://localhost:5173`    |
