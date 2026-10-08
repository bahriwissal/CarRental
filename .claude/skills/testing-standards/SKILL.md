---
name: testing-standards
description: How to write and run tests in this repo. Use whenever adding, changing or debugging tests, Gherkin scenarios, or step definitions in backend/tests.
---

# Testing standards

## Which kind of test

| You are testing | Write |
|---|---|
| Behaviour a user or the business cares about | A Gherkin scenario with a `@REQ-` tag in `tests/features/*.feature` |
| Edge cases, helpers, plumbing, regressions too low-level for a requirement | A plain pytest function in `tests/test_api.py` (or a new `tests/test_<topic>.py`) |

Default to a scenario. One behaviour per scenario; use `Scenario Outline` + `Examples` for variations of one rule.

## Writing scenarios

- One `@REQ-<AREA>-<NNN>` tag per scenario, unique across all files (`test_traceability.py` enforces it).
- Title states the rule in plain English ("A car cannot be booked twice for overlapping dates").
- Dates are relative: `"today"`, `"today+10"`, `"today-1"`. Never a calendar date.
- Cars are named `"Brand Model"` (first word = brand) and referenced by that name in later steps.
- Use `Background` for setup shared by every scenario in a file.
- Unimplemented but agreed requirements go in `backlog.feature` (feature-level `@backlog` tag).
- Any line in a feature description must not start with Given/When/Then/And/But (the parser treats it as a step).

## Available steps (reuse before adding)

Given:
- `a car "Brand Model" priced N per day` · `an unavailable car "Brand Model" priced N per day`
- `"Customer" has booked "Brand Model" from "today+A" to "today+B"` (asserts 201)

When:
- `I GET "/path"` · `I list the cars` · `I list the cars with available "true"`
- `I create a car "Brand Model" from YEAR priced N per day` · `I update car "X" with daily price N` · `I delete car "X"`
- `"Customer" books "Brand Model" from "…" to "…"` · `"Customer" books car id N from "…" to "…"`
- `"Customer" with email "…" books "Brand Model" from "…" to "…"`
- `I cancel the last booking` · `I fetch the last booking` · `I list the bookings` · `I list the bookings for car "X"`

Then:
- `the response status is N` · `the response field "f" is <JSON>` (`"ok"`, `42`, `true`) · `the response has an "f"`
- `the error detail contains "text"` (works for 4xx `detail` strings and 422 validation lists)
- `the car list is exactly "A B, C D"` · `the booking customers are "X, Y"` · `the booking total price is N`
- `car "X" no longer exists`

New steps go in `tests/test_requirements.py`, built with `step("text {name}", name=Q)` (`Q` = quoted string,
`NUM` = number), share state through the `ctx` fixture, and store the HTTP response in `ctx["response"]`.

## Plain pytest tests

- Use the `client` fixture (fresh in-memory SQLite per test) and the `make_car(**overrides)` fixture.
- Never import `SessionLocal` or touch `carrental.db` from tests.
- Assert on status code and the specific fields that matter; include `res.text` in assertion messages.

## Running

```bash
make test                     # everything implemented (backlog skipped)
make req ID=REQ-BKG-001       # one requirement, verbose
make test-backlog             # include not-yet-implemented requirements
cd backend && python -m pytest tests/test_api.py -k overlap -x   # ad hoc
```

A failing test is information: read the assertion message before changing code. Never weaken, skip or
delete a test to get green; if a test looks wrong, say so and ask.
