from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt

class NewAccomodationSchema(BaseModel):
    name: constr(min_length=2, max_length=255) # type: ignore

    capacity: PositiveInt
    maximum: PositiveInt
    quantity: PositiveInt

    day_fee: PositiveInt
    night_fee: PositiveInt
    whole_day: Union[int, None] = None

class AccomodationSchema(NewAccomodationSchema):
    id: UUID

    class Config:
        orm_mode: True  # type: ignore