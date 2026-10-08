from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CarBase(BaseModel):
    brand: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1990, le=2100)
    daily_price: float = Field(gt=0)
    available: bool = True


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=1, max_length=50)
    model: str | None = Field(default=None, min_length=1, max_length=50)
    year: int | None = Field(default=None, ge=1990, le=2100)
    daily_price: float | None = Field(default=None, gt=0)
    available: bool | None = None


class CarOut(CarBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class BookingCreate(BaseModel):
    car_id: int
    customer_name: str = Field(min_length=1, max_length=100)
    customer_email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    car_id: int
    customer_name: str
    customer_email: str
    start_date: date
    end_date: date
    total_price: float
