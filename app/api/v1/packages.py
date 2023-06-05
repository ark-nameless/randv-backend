from typing import Annotated
from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from app.schemas.packages import NewPackageSchema, PackageSchema
from app.schemas.users import UserModel
from app.utils.authentication import Authenticator
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_user
from uuid import uuid4

router = APIRouter()


@router.get(
    '', 
    summary='get all packages', 
    response_model=list[PackageSchema]
)
async def get_all_packages(db: DatabaseDep, user: UserModel = Depends(get_current_user)):
    all_packages = []
    for package in db.query(tables.Package):
        all_packages.append(PackageSchema(**package.__dict__))

    return all_packages

@router.post(
    '', 
    summary='create new package', 
    response_model=PackageSchema
)
async def create_new_package(db: DatabaseDep, payload: NewPackageSchema = Body(...), user: UserModel = Depends(get_current_user)):
    db_package = tables.Package(**dict(payload))

    print(dict(**db_package.__dict__))
    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    return PackageSchema(**dict(**db_package.__dict__))