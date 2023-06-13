from typing import List
from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.schemas.reviews import NewReviewSchema, ReviewSchema
from app.schemas.users import UserModel
from app.database.database import DatabaseDep
from app.database import tables
from app.utils.deps import get_current_active_user

from sqlalchemy import select, func


def str_to_date(val, sep='/'):
    return datetime.strptime(val.split(' ')[0], f'%d{sep}%m{sep}%Y')

def db_str_to_date(val, sep='/'):
    return datetime.strptime(val.split(' ')[0], f'%m{sep}%d{sep}%Y')


router = APIRouter()


@router.get(
    '/', 
    summary='get all payed reservations', 
)
async def get_all_paid_reservations(db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    all_reservations = []
    for package in db.query(tables.Reservation).filter(tables.Reservation.payed == True):
        all_reservations.append(package) # type: ignore

    return all_reservations


@router.get(
    '/address'
)
async def get_all_address_by_reservation(db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    all_addresses = db.query(
        tables.Reservation.address,
        func.count(tables.Reservation.address).label('total_counts')
        ).filter(tables.Reservation.payed == True).group_by(tables.Reservation.address).all()
    # statement = select([tables.Reservation.address, func.count(tables.Reservation.address)]).group_by(tables.Reservation.address)

    result =  [{'address': row[0], 'total_counts': row[1]} for row in all_addresses]

    json_result = jsonable_encoder(result)

    return json_result


@router.get(
    '/address/{start}/{end}'
)
async def get_all_address_by_reservation(start: str, end: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    start_year = start[6:10]
    end_year = end[6:10]

    all_addresses = db.query(
        tables.Reservation
        ).filter(
            tables.Reservation.payed == True, tables.Reservation.arrival.contains(start_year)
        ).all()
    
    date_start = str_to_date(start, '-')
    date_end = str_to_date(end, '-')
    result = defaultdict(int)
    print(start_year)
    for row in all_addresses:
        print(row)
        if date_start <= db_str_to_date(row.arrival) <= date_end and \
            date_start <= db_str_to_date(row.departure) <= date_end:
            result[row.address] += 1
    
    return result



@router.get(
    '/reservations/{start}/{end}'
)
async def get_all_reservations_by_date_range(start: str, end: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    start_year = start[5:9]
    end_year = end[5:9]

    all_addresses = db.query(
        tables.Reservation
        ).filter(
            tables.Reservation.payed == True, tables.Reservation.arrival.contains(start_year)
        ).all()
    
    date_start = str_to_date(start, '-')
    date_end = str_to_date(end, '-')
    
    print(f'start: {date_start}, end: {date_end}')
    result = []
    for row in all_addresses:
        print(f'{date_start} <= {str_to_date(row.arrival)} <= {date_end}')
        print(f'{date_start} <= {str_to_date(row.departure)} <= {date_end}')
        if date_start <= str_to_date(row.arrival) <= date_end and \
            date_start <= str_to_date(row.departure) <= date_end:
            print('right')
            result.append({
                'customer_name': row.customer_name,
                'guest_count': row.guest_count | 0,
                'profit': row.payment,
            })
    
    return result


@router.get(
    '/sales/{year}'
)
async def get_sales_in_year(year: str, db: DatabaseDep, user: UserModel = Depends(get_current_active_user)):
    all_addresses = db.query(
        tables.Reservation
        ).filter(
            tables.Reservation.payed == True, tables.Reservation.arrival.contains(year)
        ).all()
    
    result = defaultdict(int)
    result['January'] = 0
    result['February'] = 0
    result['March'] = 0
    result['April'] = 0
    result['May'] = 0
    result['June'] = 0
    result['July'] = 0
    result['August'] = 0
    result['September'] = 0
    result['October'] = 0
    result['November'] = 0
    result['December'] = 0
    for row in all_addresses:
        date = str_to_date(row.arrival)
        result[date.strftime("%B")] += row.payment
    
    return result