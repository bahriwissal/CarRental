import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        with TestingSession() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_car(client, **overrides):
    data = {"brand": "Renault", "model": "Clio", "year": 2022, "daily_price": 30.0, **overrides}
    res = client.post("/api/cars", json=data)
    assert res.status_code == 201
    return res.json()


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_car_crud(client):
    car = make_car(client)
    assert client.get(f"/api/cars/{car['id']}").json()["model"] == "Clio"

    res = client.patch(f"/api/cars/{car['id']}", json={"daily_price": 42})
    assert res.json()["daily_price"] == 42

    assert client.delete(f"/api/cars/{car['id']}").status_code == 204
    assert client.get(f"/api/cars/{car['id']}").status_code == 404


def test_booking_computes_price_and_rejects_overlap(client):
    car = make_car(client, daily_price=50)
    booking = {
        "car_id": car["id"],
        "customer_name": "Jane Doe",
        "customer_email": "jane@example.com",
        "start_date": "2026-11-01",
        "end_date": "2026-11-04",
    }
    res = client.post("/api/bookings", json=booking)
    assert res.status_code == 201
    assert res.json()["total_price"] == 150

    overlapping = {**booking, "start_date": "2026-11-03", "end_date": "2026-11-06"}
    assert client.post("/api/bookings", json=overlapping).status_code == 409


def test_booking_rejects_invalid_dates(client):
    car = make_car(client)
    res = client.post(
        "/api/bookings",
        json={
            "car_id": car["id"],
            "customer_name": "Jane",
            "customer_email": "jane@example.com",
            "start_date": "2026-11-05",
            "end_date": "2026-11-01",
        },
    )
    assert res.status_code == 422
