from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.accomodations import NewAccomodationSchema, AccomodationSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

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
async def create_new_accomodation(db: DatabaseDep, payload: NewAccomodationSchema = Body(...), user: UserModel = Depends(get_current_active_user)):
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


@router.put(
    '', 
    summary='update accomodation', 
    response_model=AccomodationSchema
)
async def update_accomodation(
    db: DatabaseDep,
    payload: AccomodationSchema = Body(...), 
    user: UserModel = Depends(get_current_active_user)):

    if not payload.whole_day or not payload.whole_day == 0:
        payload.whole_day = payload.day_fee + payload.night_fee
    
    found = None
    try:
        found = db.query(tables.Accomodation).filter(tables.Accomodation.id == payload.id).first()

        if not found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Accomodation with ID not found"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID"
        )

    
    found.name = payload.name
    found.capacity = payload.capacity
    found.maximum = payload.maximum
    found.quantity = payload.quantity
    found.day_fee = payload.day_fee
    found.night_fee = payload.night_fee
    found.whole_day = payload.whole_day

    db.commit()

    return payload


@router.delete(
    '/{id}',
    summary="Delete Accomodation by ID",
)
async def delete_accomodation_by_id(
    id: str, 
    db: DatabaseDep,
    user: UserModel = Depends(get_current_active_user)):

    found = None
    try: 
        found = db.query(tables.Accomodation).filter(tables.Accomodation.id == id).first()

        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accomodation with ID not Found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    db.delete(found)
    db.commit()

    return found    