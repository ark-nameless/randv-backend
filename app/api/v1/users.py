from typing_extensions import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserAuth, TokenSchema, UserModel, RegisterUser
from app.utils.authentication import Authenticator
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get(
    '',
    summary="Get all users"
)
async def get_all_users(db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    if 'admin' not in user.access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access level insufficient")
    
    all_users = []
    for db_user in db.query(tables.User):
        all_users.append(UserModel(**db_user.__dict__)) # type: ignore

    return all_users

@router.post('/signup', summary="Create new user",)
async def create_user(payload: RegisterUser, db: DatabaseDep):
    # querying database to check if user already exist
    user = db.query(tables.User).filter(tables.User.email == payload.email or tables.User.username == payload.username).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email/username already exist"
        )
    payload.password = Authenticator.hash_password(payload.password)

    db_user = tables.User(**dict(payload))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.put('/active/{id}', summary="Toggle user active status",)
async def create_user(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    # querying database to check if user already exist
    user = None
    try: 
        user = db.query(tables.User).filter(tables.User.id == id).first()
    except: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User ID")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id not found.")

    status = user.is_active
    user.is_active = not status

    db.commit()

    return user

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(db: DatabaseDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = db.query(tables.User).filter(tables.User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not Authenticator.verify_password(form_data.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    info = {
        'access': user.access,
        'is_active': user.is_active,
        'email': user.email,
        'username': user.username,
    }
    
    return {
        "access_token": create_access_token(user.username, jsonable_encoder(info)),
        "refresh_token": create_refresh_token(user.username),
    }

@router.get('/me', summary='Get details of currently logged in user', response_model=UserModel)
async def get_me(user: UserModel = Depends(get_current_active_user)):
    return user