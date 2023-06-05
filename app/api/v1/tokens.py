from fastapi import APIRouter, Depends
from app.schemas.users import UserModel
from app.schemas.tokens import TokenSchema
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.utils.deps import get_current_user
from fastapi.encoders import jsonable_encoder


router = APIRouter()

@router.get('/refresh', summary='refresh token', response_model=TokenSchema)
async def get_me(user: UserModel = Depends(get_current_user)):
    info = {
        'access': user.access,
        'is_active': user.is_active,
        'email': user.email,
        'username': user.username,
    }
    return {
        "access_token": create_access_token(user.username, jsonable_encoder(info)),
        'refresh_token': create_refresh_token(user.username)
    }