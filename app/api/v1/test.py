from typing_extensions import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserAuth, TokenSchema, UserModel
from app.utils.authentication import Authenticator
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user, DatabaseDep
from app.utils.mailer import Mailer

from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get('/test-email', summary='testing email',)
async def test_mail(db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    mail = Mailer()

    sample = db.query(tables.Reservation).filter(tables.Reservation.status == True).first()

    print(sample.__dict__)
    content = Mailer.generate_package_reservation_email(sample.customer_name, sample.arrival, sample.departure, sample.id)
    mail.send(sample.email, "Thank you for your Selecting our resort for you vacation", content)

    content = Mailer.generate_cancellation_response_email(sample.email, sample.id, sample.arrival, sample.departure)
    mail.send(sample.email, "Reservation Cancellation Request", content)

    return []