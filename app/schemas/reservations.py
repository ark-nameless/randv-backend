from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt, EmailStr

class NewReservationIndividualSchema(BaseModel):
    contact_no: constr(min_length=6) # type: ignore
    customer_name: constr(min_length=6) # type: ignore
    departure: constr(min_length=6) # type: ignore
    arrival: constr(min_length=6) # type: ignore

    email: EmailStr

    selected_accomodations: dict = {}
    selected_entrace: dict = {}
    total_amount: PositiveInt

# class EntraceFeeSchema(NewEntraceFeeSchema):
#     id: UUID

#     class Config:
#         orm_mode: True  # type: ignore