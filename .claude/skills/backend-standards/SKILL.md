---
name: backend-standards
description: Coding standards for the FastAPI/SQLAlchemy backend. Use before writing or reviewing any Python in backend/app (routers, schemas, models, database).
---

# Backend standards (FastAPI + SQLAlchemy 2.0 + Pydantic v2)

Match the existing code. When in doubt, copy the pattern from `app/routers/cars.py`.

## Layout

- One router per resource in `app/routers/<resource>.py`:
  `router = APIRouter(prefix="/api/<resource>", tags=["<resource>"])`, registered in `main.py`.
- Paths: plural nouns, no trailing slash. Collection routes use `""` (e.g. `@router.get("")`).
- Schemas live in `app/schemas.py`, named `<X>Create`, `<X>Update` (all fields optional), `<X>Out`
  (`model_config = ConfigDict(from_attributes=True)`).
- Models live in `app/models.py` with typed `Mapped[...]` / `mapped_column(...)`.

## Endpoints

- Always declare `response_model=` and, for creation, `status_code=status.HTTP_201_CREATED`.
- Deletes return `status.HTTP_204_NO_CONTENT` with no body.
- Get the session via `db: Session = Depends(get_db)`; never create `SessionLocal()` in a route.
- Look-ups that can 404 go through a `_get_<x>_or_404(db, id)` helper.
- Partial updates: `payload.model_dump(exclude_unset=True)` then `setattr`.
- Write path: `db.add(...)`, `db.commit()`, `db.refresh(obj)`, return the ORM object.

## Errors (the frontend displays `detail` verbatim)

| Situation | Status | How |
|---|---|---|
| Malformed input, field constraints, cross-field rules without DB | 422 | Pydantic `Field(...)` / `model_validator` raising `ValueError("<field> must ...")` |
| Referenced entity missing | 404 | `HTTPException(404, detail="<Thing> not found")` |
| Conflicts with current state (overlap, unavailable) | 409 | `HTTPException(409, detail="<human sentence>")` |

Error messages are short, human-readable English sentences without a trailing period.

## Queries

- SQLAlchemy 2.0 style only: `select(...)`, `db.scalars(...).all()`, `db.scalar(...)`, `db.get(Model, id)`.
- No raw SQL strings, no legacy `db.query(...)`.
- Always give list endpoints a deterministic `order_by`.
- Optional filters are optional query params (`available: bool | None = None`) applied only when not `None`.

## Style

- Python 3.10+: `X | None`, built-in generics (`list[int]`), type hints on all function signatures.
- Money is computed with `round(..., 2)`.
- Config comes from env vars with defaults (see `database.py`), never hard-coded secrets.
- `make lint` must pass (ruff, line length 110). Run `make fmt` to fix.
- No new dependency without stating why.

## Done means

`make check` passes, and any behaviour change has a `@REQ-` scenario (see `implement-requirement`).
