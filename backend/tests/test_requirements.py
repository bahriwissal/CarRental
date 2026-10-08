"""Executes every scenario in tests/features/*.feature (requirements as code).

Steps are written with regexes so quoted values never bleed into each other.
Reuse these steps when adding scenarios; add a new step only when no existing phrasing fits.
"""

import json
import re
from datetime import date, timedelta

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features")

Q = r'"(?P<{}>[^"]+)"'  # a quoted value captured as a named group
NUM = r"(?P<{}>-?\d+(?:\.\d+)?)"


def step(pattern: str, **groups: str):
    """Build a regex step parser: step('a car {name}', name=Q) -> named group 'name'."""
    for name, template in groups.items():
        pattern = pattern.replace("{" + name + "}", template.format(name))
    return parsers.re(pattern + "$")


def resolve_date(value: str) -> str:
    """'today', 'today+3', 'today-1' or an ISO date -> ISO date string."""
    m = re.fullmatch(r"today(?:([+-])(\d+))?", value)
    if not m:
        return value
    offset = int(m.group(2) or 0) * (-1 if m.group(1) == "-" else 1)
    return (date.today() + timedelta(days=offset)).isoformat()


@pytest.fixture
def ctx():
    return {"cars": {}, "bookings": [], "response": None}


# ---------- Given ----------


def _create_car(client, ctx, name, price, available=True, year=2022):
    brand, _, model = name.partition(" ")
    payload = {"brand": brand, "model": model, "year": year, "daily_price": price, "available": available}
    res = client.post("/api/cars", json=payload)
    if res.status_code == 201:
        ctx["cars"][name] = res.json()["id"]
    return res


@given(step("a car {name} priced {price} per day", name=Q, price=NUM))
def given_car(client, ctx, name, price):
    res = _create_car(client, ctx, name, float(price))
    assert res.status_code == 201, res.text


@given(step("an unavailable car {name} priced {price} per day", name=Q, price=NUM))
def given_unavailable_car(client, ctx, name, price):
    res = _create_car(client, ctx, name, float(price), available=False)
    assert res.status_code == 201, res.text


def _book(client, ctx, customer, car_id, start, end, email=None):
    payload = {
        "car_id": car_id,
        "customer_name": customer,
        "customer_email": email or f"{customer.lower()}@example.com",
        "start_date": resolve_date(start),
        "end_date": resolve_date(end),
    }
    res = client.post("/api/bookings", json=payload)
    if res.status_code == 201:
        ctx["bookings"].append(res.json()["id"])
    ctx["response"] = res
    return res


@given(step("{customer} has booked {car} from {start} to {end}", customer=Q, car=Q, start=Q, end=Q))
def given_booking(client, ctx, customer, car, start, end):
    res = _book(client, ctx, customer, ctx["cars"][car], start, end)
    assert res.status_code == 201, res.text


# ---------- When ----------


@when(step("I GET {path}", path=Q))
def when_get(client, ctx, path):
    ctx["response"] = client.get(path)


@when("I list the cars")
def when_list_cars(client, ctx):
    ctx["response"] = client.get("/api/cars")


@when(step("I list the cars with available {flag}", flag=Q))
def when_list_cars_filtered(client, ctx, flag):
    ctx["response"] = client.get("/api/cars", params={"available": flag})


@when(step("I create a car {name} from {year} priced {price} per day", name=Q, year=NUM, price=NUM))
def when_create_car(client, ctx, name, year, price):
    ctx["response"] = _create_car(client, ctx, name, float(price), year=int(year))


@when(step("I update car {name} with daily price {price}", name=Q, price=NUM))
def when_update_car(client, ctx, name, price):
    ctx["response"] = client.patch(f"/api/cars/{ctx['cars'][name]}", json={"daily_price": float(price)})


@when(step("I delete car {name}", name=Q))
def when_delete_car(client, ctx, name):
    ctx["response"] = client.delete(f"/api/cars/{ctx['cars'][name]}")


@when(step("{customer} books {car} from {start} to {end}", customer=Q, car=Q, start=Q, end=Q))
def when_book(client, ctx, customer, car, start, end):
    _book(client, ctx, customer, ctx["cars"][car], start, end)


@when(step("{customer} books car id {car_id} from {start} to {end}", customer=Q, car_id=NUM, start=Q, end=Q))
def when_book_by_id(client, ctx, customer, car_id, start, end):
    _book(client, ctx, customer, int(car_id), start, end)


@when(
    step(
        "{customer} with email {email} books {car} from {start} to {end}",
        customer=Q,
        email=Q,
        car=Q,
        start=Q,
        end=Q,
    )
)
def when_book_with_email(client, ctx, customer, email, car, start, end):
    _book(client, ctx, customer, ctx["cars"][car], start, end, email=email)


@when("I cancel the last booking")
def when_cancel_last(client, ctx):
    ctx["response"] = client.delete(f"/api/bookings/{ctx['bookings'][-1]}")


@when("I fetch the last booking")
def when_fetch_last(client, ctx):
    ctx["response"] = client.get(f"/api/bookings/{ctx['bookings'][-1]}")


@when("I list the bookings")
def when_list_bookings(client, ctx):
    ctx["response"] = client.get("/api/bookings")


@when(step("I list the bookings for car {car}", car=Q))
def when_list_bookings_for_car(client, ctx, car):
    ctx["response"] = client.get("/api/bookings", params={"car_id": ctx["cars"][car]})


# ---------- Then ----------


def _split(names: str) -> list[str]:
    return [n.strip() for n in names.split(",") if n.strip()]


@then(step("the response status is {code}", code=NUM))
def then_status(ctx, code):
    res = ctx["response"]
    assert res.status_code == int(code), f"expected {code}, got {res.status_code}: {res.text}"


@then(step("the response field {field} is (?P<value>.+)", field=Q))
def then_field(ctx, field, value):
    """value is JSON: "ok", 42, true, null."""
    assert ctx["response"].json()[field] == json.loads(value)


@then(step("the response has an {field}", field=Q))
def then_has_field(ctx, field):
    assert field in ctx["response"].json()


@then(step("the error detail contains {text}", text=Q))
def then_error_contains(ctx, text):
    detail = ctx["response"].json().get("detail")
    message = " | ".join(d.get("msg", "") for d in detail) if isinstance(detail, list) else str(detail)
    assert text in message, f"{text!r} not in {message!r}"


@then(step("the car list is exactly {names}", names=Q))
def then_car_list(ctx, names):
    got = [f"{c['brand']} {c['model']}" for c in ctx["response"].json()]
    assert got == _split(names)


@then(step("car {name} no longer exists", name=Q))
def then_car_gone(client, ctx, name):
    assert client.get(f"/api/cars/{ctx['cars'][name]}").status_code == 404


@then(step("the booking total price is {price}", price=NUM))
def then_total_price(ctx, price):
    assert ctx["response"].json()["total_price"] == float(price)


@then(step("the booking customers are {names}", names=Q))
def then_booking_customers(ctx, names):
    assert [b["customer_name"] for b in ctx["response"].json()] == _split(names)
