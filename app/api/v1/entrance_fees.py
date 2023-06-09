from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.entrance_fees import NewEntraceFeeSchema, EntraceFeeSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

router = APIRouter()


@router.get(
    '', 
    summary='get all entrace fees', 
    response_model=List[EntraceFeeSchema]
)
async def get_all_entrace_fees(db: DatabaseDep):
    all_entrace_fee = []
    for package in db.query(tables.EntraceFee):
        all_entrace_fee.append(EntraceFeeSchema(**package.__dict__)) # type: ignore

    return all_entrace_fee

@router.post(
    '', 
    summary='create new entrace fee', 
    response_model=EntraceFeeSchema
)
async def create_new_entrace_fee(db: DatabaseDep, payload: NewEntraceFeeSchema = Body(...), user: UserModel = Depends(get_current_active_user)):
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

    return EntraceFeeSchema(**dict(**db_entrace_fee.__dict__))