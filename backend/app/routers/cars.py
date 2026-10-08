from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/cars", tags=["cars"])


def _get_car_or_404(db: Session, car_id: int) -> models.Car:
    car = db.get(models.Car, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.get("", response_model=list[schemas.CarOut])
def list_cars(available: bool | None = None, db: Session = Depends(get_db)):
    query = select(models.Car).order_by(models.Car.id)
    if available is not None:
        query = query.where(models.Car.available == available)
    return db.scalars(query).all()


@router.get("/{car_id}", response_model=schemas.CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    return _get_car_or_404(db, car_id)


@router.post("", response_model=schemas.CarOut, status_code=status.HTTP_201_CREATED)
def create_car(payload: schemas.CarCreate, db: Session = Depends(get_db)):
    car = models.Car(**payload.model_dump())
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


@router.patch("/{car_id}", response_model=schemas.CarOut)
def update_car(car_id: int, payload: schemas.CarUpdate, db: Session = Depends(get_db)):
    car = _get_car_or_404(db, car_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(car, field, value)
    db.commit()
    db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = _get_car_or_404(db, car_id)
    db.delete(car)
    db.commit()
