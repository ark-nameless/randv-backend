from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
class TokenPayload(BaseModel):
    sub: Union[str, None] = None
    exp: Union[int, None] = None