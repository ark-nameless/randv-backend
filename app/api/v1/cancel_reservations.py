from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.schemas.cancel_reservation import NewReservationCancellation, ReservationCancellationSchema, ChangeRequestStatus
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user
from app.utils.mailer import Mailer

router = APIRouter()


@router.get(
    '', 
    summary='get all cancel reservations', 
    response_model=List[ReservationCancellationSchema]
)
async def get_all_cancel_reservation_request(db: DatabaseDep,
                                 user: UserModel = Depends(get_current_active_user)):
    all_entrace_fee = []
    for package in db.query(tables.CancelRequest):
        all_entrace_fee.append(ReservationCancellationSchema(**package.__dict__)) # type: ignore

    return all_entrace_fee


@router.post(
    '', 
    summary='create new cancel reservation request', 
    # response_model=
)
async def create_new_cancellation_request(db: DatabaseDep, payload: 
                                 NewReservationCancellation = Body(...)):
    try:
        reservation = db.query(tables.Reservation).filter(tables.Reservation.id == payload.reservation_id).first()
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation with ID not found"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Reservation ID"
        )
    
    found = db.query(tables.CancelRequest).filter(tables.CancelRequest.reservation_id == payload.reservation_id).first()
    if found and found.status == "rejected": #type: ignore
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Your cancel request has been rejected, Note: " + found.notes
        )
    if found:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cancel request for the same reservation already exists"
        )
    
    db_cancellation_request = tables.CancelRequest(**dict(payload))

    db.add(db_cancellation_request)
    db.commit()
    db.refresh(db_cancellation_request)

    return db_cancellation_request


@router.put(
    '/status/{id}', 
    summary='change ', 
    # response_model=
)
async def change_request_status(db: DatabaseDep, 
                                id: str, 
                                payload: ChangeRequestStatus = Body(...), 
                                user: UserModel = Depends(get_current_active_user)):

    found = db.query(tables.CancelRequest).filter(tables.CancelRequest.id == id).first()
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation cancellation with the supplied ID doesn't exists"
        )
    
    found.refund_amount = payload.refund_amount #type: ignore
    found.status = payload.status #type: ignore
    found.notes = payload.notes #type: ignore
    db.commit()

    db_reservation = db.query(tables.Reservation).filter(tables.Reservation.id == found.reservation_id).first()
    db_reservation.payment = db_reservation.total_amount - found.refund_amount
    db.commit()

    mailer = Mailer()
    content = mailer.generate_rejected_cancellation_response_email(id, db_reservation.arrival, db_reservation.departure, found.notes) if found.status == 'rejected' else mailer.generate_accepted_cancellation_response_email(id, db_reservation.arrival, db_reservation.departure, found.refund_amount, found.notes) #type: ignore

    mailer.send(db_reservation.email, "Reservation Cancellation Request", content)

    return found


