from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.comments import NewCommentSchema, CommentSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_user

router = APIRouter()


@router.get(
    '', 
    summary='get all comments', 
    response_model=List[CommentSchema]
)
async def get_all_reviews(db: DatabaseDep):
    all_entrace_fee = []
    for package in db.query(tables.Comment):
        all_entrace_fee.append(CommentSchema(**package.__dict__)) # type: ignore

    return all_entrace_fee

@router.post(
    '', 
    summary='create new comment', 
    # response_model=
)
async def create_new_comment(db: DatabaseDep, payload: NewCommentSchema = Body(...)):
    new_comment = tables.CancelRequest(**dict(payload))

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.put(
    '/toggle/{id}',
    summary='toggle comment status'
)
async def toggle_comment_status(db: DatabaseDep, id: str, user: UserModel = Depends(get_current_user)):
    found = db.query(tables.Comment).filter(tables.Comment.id == id).first()

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment with id not found'
        )

    found.status = not found.status #type: ignore
    db.commit()

    return []