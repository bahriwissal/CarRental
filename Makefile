# One entry point for humans and Claude. Run from the repo root.
# Uses backend/.venv if it exists, otherwise the system python3.
PY := $(shell [ -x backend/.venv/bin/python ] && echo .venv/bin/python || echo python3)

.PHONY: help install test test-backlog req lint fmt check frontend-install frontend-build run-api run-web

help:            ## List available targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-16s %s\n", $$1, $$2}'

install:         ## Install backend runtime + dev dependencies
	cd backend && $(PY) -m pip install -r requirements-dev.txt

test:            ## Run all implemented requirements + unit tests (backlog skipped)
	cd backend && $(PY) -m pytest

test-backlog:    ## Also run @backlog requirements (expected to fail until implemented)
	cd backend && $(PY) -m pytest --backlog

req:             ## Run one requirement, e.g. make req ID=REQ-BKG-010
	@test -n "$(ID)" || (echo "usage: make req ID=REQ-XXX-000" && exit 2)
	cd backend && $(PY) -m pytest --req $(ID) -v

lint:            ## Lint + format check (ruff)
	cd backend && $(PY) -m ruff check . && $(PY) -m ruff format --check .

fmt:             ## Auto-fix lint issues and format
	cd backend && $(PY) -m ruff check --fix . && $(PY) -m ruff format .

check: lint test ## Everything that must pass before a commit

frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend-build:  ## Build the frontend (catches JSX/import errors)
	cd frontend && npm run build

run-api:         ## Start the API on :8000 with reload
	cd backend && $(PY) -m uvicorn app.main:app --reload

run-web:         ## Start the frontend dev server on :5173
	cd frontend && npm run dev
