from typing import Union
from typing_extensions import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from pydantic import ValidationError
from app.schemas.users import TokenPayload, UserModel

from app.database.database import DatabaseDep
from app.database import tables
from app.config.config import settings

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    # scheme_name="JWT"
)


async def get_current_user(db: DatabaseDep, token: str = Depends(reuseable_oauth)) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user: Union[tables.User, None] = db.query(tables.User).filter(tables.User.username == token_data.sub).first()
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserModel(**dict(**user.__dict__))


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user