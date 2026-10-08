from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.get("", response_model=list[schemas.BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    return db.scalars(select(models.Booking).order_by(models.Booking.start_date)).all()


@router.post("", response_model=schemas.BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    car = db.get(models.Car, payload.car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    if not car.available:
        raise HTTPException(status_code=409, detail="Car is not available for rent")

    # Reject overlapping bookings for the same car
    overlap = db.scalar(
        select(models.Booking).where(
            models.Booking.car_id == car.id,
            models.Booking.start_date < payload.end_date,
            models.Booking.end_date > payload.start_date,
        )
    )
    if overlap is not None:
        raise HTTPException(status_code=409, detail="Car is already booked for these dates")

    days = (payload.end_date - payload.start_date).days
    booking = models.Booking(**payload.model_dump(), total_price=round(days * car.daily_price, 2))
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(models.Booking, booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
