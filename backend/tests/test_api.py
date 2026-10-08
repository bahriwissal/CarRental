"""Low-level API tests. Behaviour that matters to the business lives in tests/features/*.feature."""

from datetime import date, timedelta


def in_days(n: int) -> str:
    return (date.today() + timedelta(days=n)).isoformat()


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_car_crud(client, make_car):
    car = make_car()
    assert client.get(f"/api/cars/{car['id']}").json()["model"] == "Clio"

    res = client.patch(f"/api/cars/{car['id']}", json={"daily_price": 42})
    assert res.json()["daily_price"] == 42

    assert client.delete(f"/api/cars/{car['id']}").status_code == 204
    assert client.get(f"/api/cars/{car['id']}").status_code == 404


def test_booking_computes_price_and_rejects_overlap(client, make_car):
    car = make_car(daily_price=50)
    booking = {
        "car_id": car["id"],
        "customer_name": "Jane Doe",
        "customer_email": "jane@example.com",
        "start_date": in_days(10),
        "end_date": in_days(13),
    }
    res = client.post("/api/bookings", json=booking)
    assert res.status_code == 201
    assert res.json()["total_price"] == 150

    overlapping = {**booking, "start_date": in_days(12), "end_date": in_days(15)}
    assert client.post("/api/bookings", json=overlapping).status_code == 409


def test_booking_rejects_invalid_dates(client, make_car):
    car = make_car()
    res = client.post(
        "/api/bookings",
        json={
            "car_id": car["id"],
            "customer_name": "Jane",
            "customer_email": "jane@example.com",
            "start_date": in_days(14),
            "end_date": in_days(10),
        },
    )
    assert res.status_code == 422
