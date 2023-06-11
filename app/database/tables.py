from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, JSON, TIME
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import ARRAY
from sqlalchemy.sql import func
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    access = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, default='')

    logouts: Mapped[List["LogoutRecords"]] = relationship(back_populates="user")

class LogoutRecords(Base):
    __tablename__ = "logout_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship('User', back_populates='logouts')

    

class Package(Base):
    __tablename__ = "packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    image = Column(String)
    content = Column(String)

    day_fee = Column(Integer)
    night_fee = Column(Integer)
    whole_day = Column(Integer)
    
    plans = Column(ARRAY(JSON), nullable=True, default=[])

class Accomodation(Base):
    __tablename__ = "accomodations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    capacity = Column(Integer)
    maximum = Column(Integer)
    quantity = Column(Integer)
    
    day_fee = Column(Integer)
    night_fee = Column(Integer)
    whole_day = Column(Integer)

class EntraceFee(Base):
    __tablename__ = "entrace_fees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    notes = Column(String)
    day_fee = Column(Integer)
    night_fee = Column(Integer)
    whole_day = Column(Integer)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    customer_name = Column(String)
    email = Column(String)
    contact_no = Column(String)

    type = Column(String)
    package_id = Column(String, nullable=True)
    selected_time = Column(String, nullable=True)

    guest_count = Column(Integer)
    arrival = Column(String, default='', nullable=True)
    departure = Column(String, default='', nullable=True)

    payment = Column(Integer, default=0)
    total_amount = Column(Integer)
    reference_no = Column(String)

    guest_data = Column(ARRAY(JSON))
    reservation_data = Column(ARRAY(JSON))

    checked_in = Column(DateTime(timezone=True), nullable=True)
    checkout = Column(DateTime(timezone=True), nullable=True)

    payed = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    extras = Column(String, nullable=True)

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment = Column(String)
    status = Column(Boolean)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reservation_id = Column(String)
    review = Column(String)
    rating = Column(Integer, nullable=True)
    review_date = Column(DateTime, server_default=func.now())
    is_reviewed = Column(Boolean, default=False)

class CancelRequest(Base):
    __tablename__ = "cancel_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reservation_id = Column(String)
    reason = Column(String)
    status = Column(String, default="actionable") # approved, rejected, actionable
    refund_amount = Column(Integer, default=0)
    notes = Column(String, default='')



