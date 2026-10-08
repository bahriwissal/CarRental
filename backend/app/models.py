from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int]
    daily_price: Mapped[float]
    available: Mapped[bool] = mapped_column(default=True)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="car", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    customer_name: Mapped[str] = mapped_column(String(100))
    customer_email: Mapped[str] = mapped_column(String(120))
    start_date: Mapped[date]
    end_date: Mapped[date]
    total_price: Mapped[float]

    car: Mapped[Car] = relationship(back_populates="bookings")
