from fastapi import APIRouter

from app.api.v1 import users
from app.api.v1 import tokens
from app.api.v1 import packages

api_router = APIRouter()

api_router.include_router(users.router, prefix='/auth', tags=['Authentication Routes'])
api_router.include_router(tokens.router, prefix='/token', tags=['Token Configuration Routes'])
api_router.include_router(packages.router, prefix="/package", tags=['Resort Packages Management'])