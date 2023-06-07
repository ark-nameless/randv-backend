from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator

class NewPackageSchema(BaseModel):
    image: Union[str, None] = None
    content: str = Field(default='')
    day_fee: int = Field(ge=1)
    night_fee: int = Field(ge=1)
    whole_day: Union[int, None] = None
    
    @validator('day_fee', 'night_fee', 'whole_day')
    def prevent_zero(cls, v):
        if v == 0:
            raise ValueError('0 not allowed')
        return v


class PackageSchema(NewPackageSchema):
    id: UUID

    class Config:
        orm_mode: True  # type: ignore