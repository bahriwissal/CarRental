---
name: implement-requirement
description: Use whenever you add a feature, fix a behaviour bug, or implement a REQ-ID (e.g. "implement REQ-BKG-010", "add an endpoint", "customers should not be able to..."). Spec-first workflow for the Gherkin requirements in backend/tests/features.
---

# Implement a requirement (spec first)

Requirements are executable Gherkin scenarios in `backend/tests/features/`. Code changes follow them, never the reverse.

## 1. Find or write the spec

- **Given a REQ-ID**: `grep -rn "@REQ-XXX-000" backend/tests/features/`. Read the scenario and its Background.
- **Given a plain-language request**: write the scenario first.
  - Next free ID: `grep -rhoE "@REQ-[A-Z]+-[0-9]{3}" backend/tests/features | sort -u`, take the next number in the area.
  - Put it in the feature file for its area (`cars.feature`, `bookings.feature`), one `@REQ-` tag per scenario.
  - Reuse existing step phrasings from `backend/tests/test_requirements.py`. Add a new step only if none fits,
    using the `step(...)` helper with `Q`/`NUM` groups.
  - Use relative dates (`"today+10"`), never calendar dates.
  - Show the new scenario to the user before implementing if the request was ambiguous.

## 2. See it fail

```bash
make req ID=REQ-XXX-000
```

It must fail on an assertion (wrong status, missing data). If it fails with "step not found" or a
`KeyError`, the spec or step is wrong: fix that first.

## 3. Implement (smallest change)

Follow `backend-standards`. Typical placement:

| Rule type | Where |
|---|---|
| Input shape / field validation → 422 | `schemas.py` (`Field(...)`, `model_validator`) |
| Business rule needing the DB → 404/409 | the router function |
| New endpoint | the resource's router in `app/routers/` |
| New column | `models.py` + `schemas.py` (remember: delete local `carrental.db`) |

Do not edit an existing scenario to make it pass. If two requirements conflict, stop and ask.

## 4. See it pass, then everything

```bash
make req ID=REQ-XXX-000
make check
```

## 5. Close the loop

- If the scenario was in `backlog.feature`, move it (keeping its ID) into its area's feature file.
- Endpoint added or changed → update the API table in `README.md`, and `frontend/src/api.js` if the UI needs it.
- Reply with: the REQ-ID(s), files changed, and the `make check` summary line.
