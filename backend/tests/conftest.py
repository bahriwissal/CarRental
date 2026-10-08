"""Shared pytest fixtures and the requirements-as-code plumbing.

- `client`: a TestClient wired to a fresh in-memory SQLite DB per test (never touches carrental.db).
- Feature-file tags `@REQ-XXX-000` become `requirement` markers, so you can run one requirement:
      pytest --req REQ-BKG-001
- Scenarios tagged `@backlog` are specified but not implemented yet. They are skipped by default;
  run them with `pytest --backlog` (or select one with `--req`).
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


def pytest_addoption(parser):
    parser.addoption("--req", action="append", default=[], help="Only run scenarios for this requirement ID")
    parser.addoption(
        "--backlog", action="store_true", help="Also run @backlog (not yet implemented) scenarios"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "requirement(id): requirement ID a test verifies (from @REQ-* tags)")
    config.addinivalue_line("markers", "backlog: requirement specified but not implemented yet")


def pytest_bdd_apply_tag(tag, function):
    if tag.startswith("REQ-"):
        pytest.mark.requirement(tag)(function)
        return True
    return None  # default handling: the tag becomes a marker (e.g. @backlog -> backlog)


def pytest_collection_modifyitems(config, items):
    wanted = set(config.getoption("--req"))
    run_backlog = config.getoption("--backlog") or bool(wanted)

    if wanted:
        selected, deselected = [], []
        for item in items:
            ids = {m.args[0] for m in item.iter_markers("requirement")}
            (selected if ids & wanted else deselected).append(item)
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
        if not selected:
            raise pytest.UsageError(f"No scenario found for {', '.join(sorted(wanted))}")

    if not run_backlog:
        skip = pytest.mark.skip(reason="backlog requirement, not implemented yet (run with --backlog)")
        for item in items:
            if item.get_closest_marker("backlog"):
                item.add_marker(skip)


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        with TestingSession() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_car(client):
    def _make_car(**overrides):
        data = {"brand": "Renault", "model": "Clio", "year": 2022, "daily_price": 30.0, **overrides}
        res = client.post("/api/cars", json=data)
        assert res.status_code == 201, res.text
        return res.json()

    return _make_car
