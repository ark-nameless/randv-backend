from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import ARRAY
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    access = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, default='')

class Package(Base):
    __tablename__ = "packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image = Column(String)
    content = Column(String)
    day_fee = Column(Integer)
    night_fee = Column(Integer)
    whole_day = Column(Integer)

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
    contact_no = Column(String)
    email = Column(String)
    type = Column(String)
    package_id = Column(String)

    arrival = Column(DateTime(timezone=True))
    departure = Column(DateTime(timezone=True))
    guest_count = Column(Integer)
    payment = Column(Integer, default = 0)
    total_amount = Column(Integer)
    
    checked_in = Column(DateTime(timezone=True))
    checkout = Column(DateTime(timezone=True))

    selected_accomodations = Column(ARRAY(JSON))
    guest_entrace = Column(ARRAY(JSON))

    payed = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    extras = Column(String)


