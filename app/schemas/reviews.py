import datetime
from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt, EmailStr

class NewReviewSchema(BaseModel):
    reservation_id: str
    review: str = ''
    rating: Union[int, None] = None

class ReviewSchema(NewReviewSchema):
    id = UUID
    review_date: datetime.datetime
    is_reviewed: bool
