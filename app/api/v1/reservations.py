from typing import List

from fastapi import APIRouter, Body, Depends
from app.schemas.reservations import NewReservationIndividualSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_user

router = APIRouter()


@router.get(
    '', 
    summary='get all reservations', 
    response_model=List[dict]
)
async def get_all_reservations(db: DatabaseDep, user: UserModel = Depends(get_current_user)):
    return []

@router.post(
    '/individual', 
    summary='create new package', 
    # response_model=NewReservationIndividualSchema
)
async def create_new_reservation(db: DatabaseDep, payload: dict = Body(...)):

    print(payload)
    return []


