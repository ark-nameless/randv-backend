from typing import Union
import uuid

from typing_extensions import Annotated
from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserAuth, TokenSchema, UserModel, RegisterUser, ForgetUserPassword, PasswordReset
from app.utils.authentication import Authenticator
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user
from app.utils.uuid_slug import ID
from app.utils.mailer import Mailer

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
async def create_user(payload: RegisterUser, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
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

@router.put(
    '/password/forgot',
    summary="Set user token to setup for password reset"
)
async def forgot_password(payload: ForgetUserPassword, db: DatabaseDep):
    user: Union[tables.User, None] = None
    try: 
        user = db.query(tables.User).filter(tables.User.email == payload.email).first()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with email not found")
    
    token = None
    
    if user.reset_token:
        token = user.reset_token
    else:
        token = ID.uuid2slug(str(uuid.uuid4()))
    
    user.reset_token = token
    db.commit()

    mailer = Mailer()
    content = mailer.generate_password_reset_email(user.username, token)
    mailer.send(db.email, "Password Reset", content)

    return []

@router.put(
    '/password/reset/{token}',
    summary="change user password"
)
async def change_user_password(token: str, db: DatabaseDep, payload: PasswordReset = Body(...),):
    user: Union[tables.User, None] = None
    try: 
        user = db.query(tables.User).filter(tables.User.reset_token == token).first()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password reset token not found")
    
    user.reset_token = None
    user.password = Authenticator.hash_password(payload.password)    
    db.commit()

    return []

    


@router.put('/active/{id}', summary="Toggle user active status",)
async def toggle_user_active_status(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
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
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your Account has been deactivated, please contact your admin for more query"
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