from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Car

SAMPLE_CARS = [
    {"brand": "Renault", "model": "Clio", "year": 2022, "daily_price": 35.0},
    {"brand": "Peugeot", "model": "208", "year": 2023, "daily_price": 40.0},
    {"brand": "Dacia", "model": "Duster", "year": 2021, "daily_price": 45.0},
    {"brand": "Toyota", "model": "Corolla", "year": 2023, "daily_price": 55.0},
]


def seed_if_empty(db: Session) -> None:
    if db.scalar(select(Car).limit(1)) is None:
        db.add_all(Car(**data) for data in SAMPLE_CARS)
        db.commit()
