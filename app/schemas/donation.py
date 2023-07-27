from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, validator


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int

    class Config:
        extra = Extra.forbid
        orm_mode = True

    @validator('create_date')
    def edit_create_date(cls, value):
        return value.isoformat(timespec='auto')


class DonationAll(DonationDB):
    invested_amount: Optional[int]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]
