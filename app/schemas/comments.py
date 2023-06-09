from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, constr, PositiveInt, EmailStr

class NewCommentSchema(BaseModel):
    comment: constr(min_length=6) #type: ignore

class CommentSchema(NewCommentSchema):
    id: UUID