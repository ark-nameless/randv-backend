from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.accomodations import NewAccomodationSchema, AccomodationSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_user

router = APIRouter()


@router.get(
    '', 
    summary='get all accomodations', 
    response_model=List[AccomodationSchema]
)
async def get_all_accomodations(db: DatabaseDep):
    all_packages = []
    for package in db.query(tables.Accomodation):
        all_packages.append(AccomodationSchema(**package.__dict__)) # type: ignore

    return all_packages

@router.post(
    '', 
    summary='create new accomodations', 
    response_model=AccomodationSchema
)
async def create_new_accomodation(db: DatabaseDep, payload: NewAccomodationSchema = Body(...), user: UserModel = Depends(get_current_user)):
    if not payload.whole_day or not payload.whole_day == 0:
        payload.whole_day = payload.day_fee + payload.night_fee

    found = db.query(tables.Accomodation).filter(tables.Accomodation.name == payload.name).first()
    if found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Accomodation with the same name already exists"
        )
    db_package = tables.Accomodation(**dict(payload))

    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    return AccomodationSchema(**dict(**db_package.__dict__))