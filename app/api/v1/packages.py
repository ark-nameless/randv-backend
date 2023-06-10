from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.packages import NewPackageSchema, PackageSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

router = APIRouter()


@router.get(
    '', 
    summary='get all packages', 
    response_model=List[PackageSchema]
)
async def get_all_packages(db: DatabaseDep):
    all_packages = []
    for package in db.query(tables.Package):
        all_packages.append(PackageSchema(**package.__dict__)) #type: ignore

    return all_packages

@router.get(
    '/{id}',
    summary='get package by id',
    response_model=PackageSchema
)
async def get_package_by_id(id: str, db: DatabaseDep):
    package = db.query(tables.Package).filter(tables.Package.id == id).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Package with not found."
        )

    return PackageSchema(**package.__dict__)


@router.post(
    '', 
    summary='create new package', 
    response_model=PackageSchema
)
async def create_new_package(db: DatabaseDep, payload: NewPackageSchema = Body(...), user: UserModel = Depends(get_current_active_user)):
    db_package = tables.Package(**dict(payload))

    print(dict(**db_package.__dict__))
    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    return PackageSchema(**dict(**db_package.__dict__))

@router.delete(
    '/{id}',
    summary="Remove package",
)
async def remove_package_by_id(db: DatabaseDep, id: str, user: UserModel = Depends(get_current_active_user)):
    found = None
    try:
        found = db.query(tables.Package).filter(tables.Package.id == id).first()
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="package with id not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID")

    db.delete(found)
    db.commit()

    return []