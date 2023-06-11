from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.entrance_fees import NewEntranceFeeSchema, EntranceFeeSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

router = APIRouter()


@router.get(
    '', 
    summary='get all entrace fees', 
    response_model=List[EntranceFeeSchema]
)
async def get_all_entrace_fees(db: DatabaseDep):
    all_entrace_fee = []
    for package in db.query(tables.EntraceFee):
        all_entrace_fee.append(EntranceFeeSchema(**package.__dict__)) # type: ignore

    return all_entrace_fee

@router.post(
    '', 
    summary='create new entrace fee', 
    response_model=EntranceFeeSchema
)
async def create_new_entrace_fee(db: DatabaseDep, payload: NewEntranceFeeSchema = Body(...), user: UserModel = Depends(get_current_active_user)):
    if not payload.whole_day:
        payload.whole_day = payload.day_fee + payload.night_fee

    found = db.query(tables.EntraceFee).filter(tables.EntraceFee.name == payload.name).first()
    if found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Entrace fee with the same name already exists"
        )
    db_entrace_fee = tables.EntraceFee(**dict(payload))

    db.add(db_entrace_fee)
    db.commit()
    db.refresh(db_entrace_fee)

    return EntranceFeeSchema(**dict(**db_entrace_fee.__dict__))




@router.put(
    '', 
    summary='update entrace fee', 
    response_model=EntranceFeeSchema
)
async def update_accomodation(
    db: DatabaseDep,
    payload: EntranceFeeSchema = Body(...), 
    user: UserModel = Depends(get_current_active_user)):
    
    found = None
    try:
        found = db.query(tables.EntraceFee).filter(tables.EntraceFee.id == payload.id).first()

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
    found.notes = payload.notes
    found.day_fee = payload.day_fee
    found.night_fee = payload.night_fee
    found.whole_day = payload.whole_day

    db.commit()

    return payload


@router.delete(
    '/{id}',
    summary="Delete Entrace Fee by ID",
)
async def delete_accomodation_by_id(
    id: str, 
    db: DatabaseDep,
    user: UserModel = Depends(get_current_active_user)):

    found = None
    try: 
        found = db.query(tables.EntraceFee).filter(tables.EntraceFee.id == id).first()

        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrace Fee with ID not Found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    db.delete(found)
    db.commit()

    return found    