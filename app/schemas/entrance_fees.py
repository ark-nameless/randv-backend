from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt

class NewEntraceFeeSchema(BaseModel):
    name: constr(min_length=2, max_length=255) # type: ignore
    notes: constr(min_length=2, max_length=255) # type: ignore
    day_fee: PositiveInt
    night_fee: PositiveInt
    whole_day: Union[int, None] = None

class EntraceFeeSchema(NewEntraceFeeSchema):
    id: UUID

    class Config:
        orm_mode: True  # type: ignore