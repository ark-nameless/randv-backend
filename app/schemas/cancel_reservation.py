from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt, EmailStr

class NewReservationCancellation(BaseModel):
    reservation_id: constr(min_length=6) #type: ignore
    reason: str = ''

class ReservationCancellationSchema(NewReservationCancellation):
    id: UUID
    status: constr(min_length=6) # approved, rejected, actionable
    notes: str = ''

class ChangeRequestStatus(BaseModel):
    status: constr(min_length=2) # approved, rejected, actionable
    notes: str = ''