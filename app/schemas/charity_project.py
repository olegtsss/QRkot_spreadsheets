from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.config import settings


NAME_IS_SPACE = '{name} не может пустой строкой!'


def check_value_isspace(value, name):
    if value.isspace():
        raise ValueError(NAME_IS_SPACE.format(name=name))
    return value


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=settings.charity_project_name_max)
    description: str
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid

    @validator('name')
    def name_cant_be_spaces(cls, value: str):
        return check_value_isspace(value, 'Имя')

    @validator('description')
    def description_cant_be_spaces(cls, value: str):
        return check_value_isspace(value, 'Описание')


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True

    @validator('create_date')
    def edit_create_date(cls, value):
        return value.isoformat(timespec='auto')


class CharityProjectCreate(CharityProjectBase):
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    name: str = Field(None, max_length=settings.charity_project_name_max)
    description: Optional[str]
