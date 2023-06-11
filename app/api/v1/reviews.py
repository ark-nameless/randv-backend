from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.reviews import NewReviewSchema, ReviewSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

router = APIRouter()


@router.get(
    '', 
    summary='get all reviews', 
    response_model=List[ReviewSchema]
)
async def get_all_review(db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    all_entrace_fee = []
    for package in db.query(tables.Review):
        all_entrace_fee.append(ReviewSchema(**package.__dict__)) # type: ignore

    return all_entrace_fee

@router.post(
    '', 
    summary='create new review', 
    # response_model=
)
async def create_new_review(db: DatabaseDep, payload: NewReviewSchema = Body(...)):
    new_review = tables.Review(**dict(payload))

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review

@router.put(
    '/toggle/{id}',
    summary='toggle review status'
)
async def toggle_review_status(db: DatabaseDep, id: str, user: UserModel = Depends(get_current_active_user)):
    found = db.query(tables.Comment).filter(tables.Comment.id == id).first()

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment with id not found'
        )

    found.is_reviewed = not found.is_reviewed 
    db.commit()

    return []