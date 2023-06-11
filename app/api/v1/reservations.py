from typing import List
from collections import defaultdict

from datetime import datetime, timedelta
from fastapi import APIRouter, Body, Depends, status, HTTPException
from app.schemas.reservations import NewReservationIndividualSchema, NewPackageReservationSchema, SetReservationPayment
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.exceptions.exceptions import JSONException
from app.database import tables
import pprint
from app.utils.deps import get_current_active_user
from app.utils.mailer import Mailer

router = APIRouter()

individual_time = {
    'day': {
        'start': '6:01 AM',
        'end': '7:00 PM'
    },
    'night': {
        'start': '5:01 PM',
        'end': '5:00 AM'
    },
    'whole': {
        'start': '6:01 AM',
        'end': '5:00 AM'
    }
}

def date_in_range(start: str, end: str, key: str):
    return str_to_date(start) < str_to_date(key) < str_to_date(end) or \
            str_to_date(start) < str_to_date(key) < str_to_date(end)

def get_datetime(session, date, time):
    date = datetime.strptime(date, '%m/%d/%Y')
    if session == 'night' and time == 'end':
        date = date + timedelta(days=1)
    return datetime.strptime(f"{date.strftime('%m/%d/%Y')} {individual_time[session][time]}", '%m/%d/%Y %I:%M %p')


def str_to_datetime(val):
    return datetime.strptime(val, '%m/%d/%Y %I:%M %p')

def str_to_date(val):
    return datetime.strptime(val.split(' ')[0], '%m/%d/%Y')

def date_in_range(arrival1, departure1, arrival2,  departure2):
    return str_to_date(arrival1) <= str_to_date(arrival2) < str_to_date(departure1) or \
    str_to_date(arrival1) <= str_to_date(departure2) < str_to_date(departure1) or \
    str_to_date(arrival2) <= str_to_date(arrival1) < str_to_date(departure2) or \
    str_to_date(arrival2) <= str_to_date(departure1) < str_to_date(departure2)


@router.get(
    '/valid/{id}',
    summary="Check if the id is a valid reservation"
)
async def check_if_reservation_id_is_valid(id: str, db: DatabaseDep) :
    try:
        found = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()
        
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation ID not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    
    return []


@router.get(
    '/{id}',
    summary="Check if the id is a valid reservation"
)
async def get_reservation_by_id(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)) :
    found = None
    try:
        found = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()
        
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation ID not found")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    
    return found

@router.get(
    '', 
    summary='get all reservations', 
    response_model=List[dict]
)
async def get_all_reservations(db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    all_reservations = []
    for package in db.query(tables.Reservation):
        all_reservations.append(dict(**package.__dict__)) #type: ignore

    return all_reservations


@router.post(
    '/check',
    summary='check if reservation is available'
)
async def check_if_reservation_is_available(db: DatabaseDep, payload: dict = Body(...)):
    pprint.pprint(payload)

    arrival = payload['arrival']
    departure = payload['departure'] if payload['departure'] else payload['arrival']

    date = datetime.strptime(payload['arrival'], '%m/%d/%Y')
    date = datetime.strftime(date, '%m/%d/%Y')

    arrival = datetime.strptime(arrival, '%m/%d/%Y')
    arrival = datetime.strftime(arrival, '%m/%d/%Y')

    departure = datetime.strptime(departure, '%m/%d/%Y')
    departure = datetime.strftime(departure, '%m/%d/%Y')
    db_reservations = db.query(tables.Reservation).filter(tables.Reservation.status == True).all()

    same_day_reservation = [reservation for reservation in db_reservations if date in reservation.arrival]

    # Checking customer infos
    if not 'selected_time' in payload and not 'selected_accomodations' in payload:
        for reservation in db_reservations:
            # print(f'{str_to_date(reservation.arrival)} <= {str_to_date(arrival)} <= {str_to_date(reservation.departure)}')

            if date_in_range(reservation.arrival, reservation.departure, arrival, departure):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Reservation with Selected date and time isn't available, please selecte new date or time"
                )
        return []
            
    # if trying to book a package but there is a reservation for individual, return false
    if payload['type'] =='package' and payload['selected_time'] == 'whole' and len(same_day_reservation) > 0:
        print("payload['selected_time'] == 'whole' and len(same_day_reservation) > 0 and payload['type'] == 'package'")
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reservation with Selected date and time isn't available, please selecte new date or time"
            )
    

    if payload['type'] == 'package' or payload['type'] == 'individual': 
        arrival = payload['arrival']
        departure = payload['departure'] if payload['departure'] else payload['arrival']

        arrival = datetime.strptime(arrival, '%m/%d/%Y')
        arrival = datetime.strftime(arrival, '%m/%d/%Y')

        departure = datetime.strptime(departure, '%m/%d/%Y')
        departure = datetime.strftime(departure, '%m/%d/%Y')

        list_of_accomodations = defaultdict()
        db_accomodations = db.query(tables.Accomodation).all()
        for accomodation in db_accomodations:
            list_of_accomodations[str(accomodation.id)] = accomodation.quantity


        for reservation in db_reservations: 
            if payload['type'] == 'individual':
                list_of_accomodation = list_of_accomodations
                selected_accomodations = payload['selected_accomodations']
                for selected_accomodation in selected_accomodations:
                    db_accomodation = db.query(tables.Accomodation).filter(tables.Accomodation.id == selected_accomodation['id']).first()
                    if reservation.type == 'individual':
                        for reservation_plan in reservation.reservation_data:
                            list_of_accomodation[reservation_plan['id']] -= reservation_plan['quantity']
                            list_of_accomodation[selected_accomodation['id']] -= selected_accomodation['reserveQuantity']
                            print(list_of_accomodation)
                            if list_of_accomodation[reservation_plan['id']] < 0 or list_of_accomodation[selected_accomodation['id']] < 0:
                                print("list_of_accomodation[reservation_plan['id']] <= 0 or list_of_accomodation[selected_accomodation['id']] <= 0:")
                                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                            if reservation_plan['id'] == selected_accomodation['id']:
                                # check the arrival time first
                                if date_in_range(reservation_plan['start_time'], reservation_plan['end_time'], arrival):
                                    if reservation_plan['type'] == selected_accomodation['selectedTime'] or \
                                        selected_accomodation['selectedTime'] == 'whole' or reservation_plan['type'] == 'whole': #type: ignore
                                        print("date_in_range(reservation_plan['start_time'], reservation_plan['end_time'], arrival):")
                                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                                if date_in_range(reservation_plan['start_time'], reservation_plan['end_time'], departure):
                                    if reservation_plan['type'] == selected_accomodation['selectedTime'] or \
                                        selected_accomodation['selectedTime'] == 'whole' or reservation_plan['type'] == 'whole': #type: ignore
                                        print("date_in_range(reservation_plan['start_time'], reservation_plan['end_time'], departure):")
                                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                            
            if reservation.type == 'package' and payload['type'] == 'package':
                selected_package = db.query(tables.Package).filter(tables.Package.id == payload['package_id']).first()
                selected_plan = [package for package in selected_package.plans if package['type'] == payload['selected_time']][0]
                if date_in_range(reservation.arrival, reservation.departure, arrival):
                    if reservation.type != payload['type']:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                    if reservation.selected_time == payload['selected_time'] or \
                        payload['selected_time'] == 'whole' or reservation.selected_time: #type: ignore
                        print("date_in_range(reservation_plan['start_time'], reservation_plan['end_time'], arrival): package")
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                    
                if date_in_range(reservation.arrival, reservation.departure, departure):
                    if reservation.type != payload['type']:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                    if reservation.selected_time == payload['selected_time'] or \
                        payload['selected_time'] == 'whole' or reservation.selected_time: #type: ignore
                        print("date_in_range(reservation_plan['start_time'], reservation_plan['end_time'], departure): package")
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reservation with Selected date and time isn't available, please selecte new date or time")
                    
                if date_in_range(reservation.arrival, reservation.departure, arrival, departure):
                    if reservation.selected_time == 'whole' or reservation.selected_time == payload['selected_time'] or \
                        payload['selected_time'] == 'whole':
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Reservation with Selected date and time isn't available, please selecte new date or time"
                        )

    return []


@router.post(
    '/package', 
    summary='create new package reservation', 
    # response_model=NewReservationIndividualSchema
)
async def create_new_package_reservation(db: DatabaseDep, 
                                         id: str, 
                                         payload: NewPackageReservationSchema):
    arrival = payload.arrival
    departure = payload.departure if payload.departure else payload.arrival

    db_package = db.query(tables.Package).filter(tables.Package.id == payload.package_id).first()
    selected_plan = [package for package in db_package.plans if package['type'] == payload.selected_time][0] #type:ignore

    reservation_info = {
        'customer_name': payload.customer_name,
        'email': payload.email,
        'contact_no': payload.contact_no,
        'type': 'package',

        'arrival': datetime.strftime(get_datetime(payload.selected_time, arrival, 'start'), '%m/%d/%Y %I:%M %p'),
        'departure': datetime.strftime(get_datetime(payload.selected_time, arrival, 'end'), '%m/%d/%Y %I:%M %p'),

        'selected_time': payload.selected_time,
        'total_amount': selected_plan['price'], # type: ignore
        'reference_no': payload.reference_no,
        'package_id': payload.package_id,
    }

    pprint.pprint(reservation_info)

    db_reservation = tables.Reservation(**reservation_info) # type: ignore
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    mail = Mailer()
    content = Mailer.generate_package_reservation_email(db_reservation.customer_name, db_reservation.arrival, db_reservation.departure, db_reservation.id)
    mail.send(db_reservation.email, "Thank you for your Selecting our resort for you vacation", content)

    return db_reservation

@router.post(
    '/individual', 
    summary='create new individual reservation', 
    # response_model=NewReservationIndividualSchema
)
async def create_new_individual_reservation(db: DatabaseDep, payload: dict = Body(...)):
    pprint.pprint(payload)
    arrival = payload['arrival']
    departure = payload['departure'] if payload['departure'] else payload['arrival']

    # get_datetime = lambda session, date, time: datetime.strptime(f'{date} {individual_time[session][time]}', '%m/%d/%Y %I:%M %p')

    guest_entrace = [
        {
            'name': a['name'],
            'type': a['selectedTime'], 
            'price': a['selectedPlan']['price'],
            'total': a['total'],
            'quantity': a['reserveQuantity'],
         } for a in payload['selected_accomodations']]
    reservations = [
        {
            'id': r['id'],
            'quantity': r['reserveQuantity'],
            'start_time': datetime.strftime(get_datetime(r['selectedTime'], arrival, 'start'), '%m/%d/%Y %I:%M %p'),
            'end_time': datetime.strftime(get_datetime(r['selectedTime'], arrival, 'end'), '%m/%d/%Y %I:%M %p'),
            'type': r['selectedTime'],
        }
        for r in payload['selected_accomodations']
    ]
    pprint.pprint(payload['selected_accomodations'])
    guest_count = sum([g['quantity'] for g in guest_entrace])
    reservation_info = {
        'customer_name': payload['customer_name'],
        'email': payload['email'],
        'contact_no': payload['contact_no'],
        'type': 'individual',

        'guest_count': guest_count,
        'arrival': payload['arrival'],
        'departure': payload['departure'] if payload['departure'] else payload['arrival'],

        'guest_data': guest_entrace,
        'reservation_data': reservations,

        'total_amount': payload['total_amount'],
        'reference_no': payload['reference_no'],
    }

    db_reservation = tables.Reservation(**reservation_info) #type: ignore

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    mail = Mailer()
    content = Mailer.generate_package_reservation_email(db_reservation.customer_name, db_reservation.arrival, db_reservation.departure, db_reservation.id)
    mail.send(db_reservation.email, "Thank you for your Selecting our resort for you vacation", content)

    return db_reservation


@router.put(
    '/checkin/{id}', 
    summary='set current timestamp to customer checkin status', 
)
async def check_in_guest_with_id(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    db_reservation = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()

    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reservation with given id not found',
        )
    
    db_reservation.checked_in = datetime.now()
    db.commit()
    return []

@router.put(
    '/checkout/{id}', 
    summary='set current timestamp to customer checkout status', 
)
async def check_out_guest_with_id(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    db_reservation = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()

    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reservation with given id not found',
        )
    
    db_reservation.checkout = datetime.now()
    db_reservation.status = False
    db.commit()

    mailer = Mailer()

    content = mailer.generate_check_out_thank_you_email(db_reservation.email, db_reservation.id)
    mailer.send(db_reservation.email, "R & V Private Resort Checkout", content)

    return []

@router.put(
    '/cancel/{id}', 
    summary='cancel reservation', 
)
async def cancel_reservation(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    db_reservation = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()

    if not 'admin' in user.access :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Insufficient access level'
        )

    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reservation with given id not found',
        )
    
    db_reservation.payment = 0
    db_reservation.payed = False
    db_reservation.status = False
    db.commit()
    return []


@router.put(
    '/paid/toggle/{id}', 
    summary='change paid status', 
)
async def toggle_payment_reservation_status(id: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    db_reservation = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()

    if not 'admin' in user.access:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient access level"
        )

    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reservation with given id not found',
        )
    pay_status = db_reservation.payed
    db_reservation.payed = not pay_status
    db_reservation.status = not pay_status

    if db_reservation.status:
        db_reservation.payment = db_reservation.total_amount
    else:
        db_reservation.payment = 0
    db.commit()

    return []


@router.put(
    '/payment/{id}', 
    summary='Set payment for reservation by reservation id', 
)
async def toggle_payment_reservation_status(id: str, db: DatabaseDep,
                                            payload: SetReservationPayment = Body(...),
                                            user: UserModel = Depends(get_current_active_user)):

    db_reservation = None

    try:
        db_reservation = db.query(tables.Reservation).filter(tables.Reservation.id == id).first()
    except: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Reservation ID")

    if not 'admin' in user.access:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient access level"
        )

    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reservation with given id not found',
        )
    
    db_reservation.payed = payload.payed
    db_reservation.payment = payload.payment
    db_reservation.total_amount = payload.total_amount
    db.commit()

    mailer = Mailer()
    content = mailer.generate_payment_accepted_email(db_reservation.customer_name, db_reservation.id, db_reservation.payment)

    mailer.send(db_reservation.email, "R & V Private Resort Payment Accepted", content)

    return db_reservation






