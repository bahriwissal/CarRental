# CarRental: context for Claude

Car rental web app. **FastAPI + SQLAlchemy 2.0 + SQLite** backend, **React 18 + Vite** frontend.
Customers browse cars and book them for a date range; the API computes the price and rejects overlaps.

## Commands (run from repo root)

| Goal | Command |
|---|---|
| Install backend deps | `make install` |
| Run all tests (must stay green) | `make test` |
| Run one requirement | `make req ID=REQ-BKG-010` |
| Run backlog (unimplemented) requirements | `make test-backlog` |
| Lint + format check | `make lint` · auto-fix: `make fmt` |
| **Before every commit** | `make check` (lint + tests) |
| Frontend build check | `make frontend-install && make frontend-build` |
| Run the app | `make run-api` (port 8000) · `make run-web` (port 5173) |

Never claim a task is done until `make check` passes; paste the summary line in your reply.

## Where things are

```
backend/app/main.py           FastAPI app, CORS, lifespan (create_all + seed)
backend/app/models.py         SQLAlchemy models: Car, Booking
backend/app/schemas.py        Pydantic: <X>Create / <X>Update / <X>Out
backend/app/routers/          one router per resource, prefix /api/<resource>
backend/tests/features/       REQUIREMENTS AS CODE: Gherkin, one @REQ-ID per scenario
backend/tests/test_requirements.py   step definitions that execute the .feature files
backend/tests/test_traceability.py   enforces one unique @REQ tag per scenario
backend/tests/test_api.py     low-level API tests
backend/tests/conftest.py     `client` (in-memory DB) + `make_car` fixtures, --req/--backlog options
frontend/src/api.js           the ONLY place that calls fetch
frontend/src/components/      CarList, BookingForm, BookingList
```

## Requirements are the source of truth

- Requirements live in `backend/tests/features/*.feature`, each scenario tagged `@REQ-<AREA>-<NNN>`
  (areas: `SYS`, `CAR`, `BKG`; add a new area if needed). IDs are never reused or renumbered.
- `backlog.feature` holds agreed requirements that are **not implemented yet** (skipped by `make test`).
- To implement or change behaviour, follow the `implement-requirement` skill: spec first, see it fail,
  implement, see it pass, move it out of the backlog, `make check`.
- If a request conflicts with an existing scenario, stop and ask instead of editing the scenario to fit.

## Domain rules (enforced by the specs)

- Booking price = nights × `daily_price`, nights = `end_date - start_date` (end date is exclusive).
- Overlap check: an existing booking overlaps if `existing.start < new.end and existing.end > new.start`,
  so back-to-back bookings are allowed.
- `end_date <= start_date` → 422 (schema validator). Unknown car → 404. Unavailable or overlapping → 409.
- Deleting a car cascades to its bookings.

## Conventions

- Backend standards: see `.claude/skills/backend-standards`. Tests: `.claude/skills/testing-standards`.
  Frontend: `.claude/skills/frontend-standards`.
- Error contract: `HTTPException(status_code, detail="<Thing> not found")`; the frontend shows `detail`.
- Keep the README API table in sync when you add or change an endpoint.

## Gotchas

- **No migrations.** Tables come from `Base.metadata.create_all` at startup. If you change `models.py`,
  delete `backend/carrental.db` before running the app locally (tests use in-memory SQLite and are unaffected).
- Tests never touch `carrental.db`: always use the `client` fixture, never `SessionLocal` directly.
- Specs use relative dates (`"today+10"`) so they never expire; do not hard-code calendar dates in tests.
- `backend/package-lock.json` is an empty stray file; ignore it.
- Frontend targets Node 16 (`.nvmrc`), so do not add dependencies that need a newer Node without asking.
- Do not add new dependencies (Python or npm) without saying why in your reply.
