from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt, EmailStr

class NewReservationIndividualSchema(BaseModel):
    contact_no: constr(min_length=6) # type: ignore
    customer_name: constr(min_length=6) # type: ignore
    arrival: constr(min_length=6) # type: ignore
    departure: constr(min_length=0) # type: ignore

    email: EmailStr

    selected_accomodations: dict = {}
    selected_entrace: dict = {}
    total_amount: PositiveInt

class NewPackageReservationSchema(BaseModel):
    contact_no: constr(min_length=6) # type: ignore
    customer_name: constr(min_length=2) # type: ignore
    arrival: constr(min_length=2) # type: ignore
    departure: constr(min_length=0) # type: ignore
    email: EmailStr
    package_id: constr(min_length=35) # type: ignore
    reference_no: constr(min_length=6) # type: ignore
    selected_time: constr(min_length=2) # type: ignore

class NewReservationCancellation(BaseModel):
    reservation_id: constr(min_length=6)
    reason = constr(min_length=6)

class ReservationCancellation(NewReservationCancellation):
    id: str
    status = constr(min_length=6) # approved, rejected, actionable
    notes: str = ''

# class EntraceFeeSchema(NewEntraceFeeSchema):
#     id: UUID

#     class Config:
#         orm_mode: True  # type: ignore