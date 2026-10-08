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

Run the tests:

```bash
pytest
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

## Configuration

| Variable       | Default                    |
|----------------|----------------------------|
| `DATABASE_URL` | `sqlite:///./carrental.db` |
| `CORS_ORIGINS` | `http://localhost:5173`    |
