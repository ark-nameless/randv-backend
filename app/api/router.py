from fastapi import APIRouter

from app.api.v1 import users
from app.api.v1 import tokens
from app.api.v1 import packages
from app.api.v1 import entrance_fees
from app.api.v1 import accomodations
from app.api.v1 import reservations
from app.api.v1 import cancel_reservations
from app.api.v1 import comments
from app.api.v1 import reviews

api_router = APIRouter()

api_router.include_router(users.router, prefix='/auth', tags=['Authentication Routes'])
api_router.include_router(tokens.router, prefix='/token', tags=['Token Configuration Routes'])
api_router.include_router(packages.router, prefix="/package", tags=['Resort Packages Management'])
api_router.include_router(entrance_fees.router, prefix="/entrace-fee", tags=['Resort Entrace Fee Management'])
api_router.include_router(accomodations.router, prefix="/accomodation", tags=['Resort Accomodation Management'])
api_router.include_router(reservations.router, prefix="/reservation", tags=['Resort Reservation Management'])
api_router.include_router(cancel_reservations.router, prefix="/cancel", tags=['Resort Reservation Cancellation Management'])
api_router.include_router(comments.router, prefix="/comments", tags=['Resort Comments Management'])
api_router.include_router(reviews.router, prefix="/reviews", tags=['Resort Reviews Management'])