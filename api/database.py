import datetime
import os
import time
from uuid import UUID

import redis
import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as UUIDP
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DATABASE_URL = os.getenv("POSTGRES_CONN")
while True:
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        break

    except sqlalchemy.exc.OperationalError:
        time.sleep(1)


class User_table(Base):
    __tablename__ = "users"

    user_id: UUID = Column(UUIDP(as_uuid=True), primary_key=True)
    login: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    age: int = Column(Integer, nullable=False)
    about: str = Column(Text, nullable=True)
    contact: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, nullable=False)
    avatar: bytes = Column(LargeBinary)

class Mentor_table(Base):
    __tablename__ = "mentors"

    mentor_id: UUID = Column(UUIDP(as_uuid=True), primary_key=True)
    user_id: UUID = Column(UUIDP(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    direction: str = Column(String, nullable=False)

class Students_table(Base):
    __tablename__ = "students"

    id: UUID = Column(UUIDP(as_uuid=True), primary_key=True)
    mentor_id: UUID = Column(UUIDP(as_uuid=True), ForeignKey('mentors.mentor_id', ondelete='CASCADE'), nullable=False)
    user_id: UUID = Column(UUIDP(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

class Admin_table(Base):
    __tablename__ = "admins"

    admin_id = Column(UUIDP(as_uuid=True), primary_key=True)
    login: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)

class Mentors_requests_table(Base):
    __tablename__ = "mentorRequests"

    request_id: UUID = Column(UUIDP(as_uuid=True), primary_key=True)
    user_id: UUID = Column(UUIDP(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    about: str = Column(Text, nullable=False)
    direction: str = Column(String, nullable=False)
    date: datetime.datetime = Column(TIMESTAMP, nullable=False)
    status: bool = Column(Boolean, nullable=True)

class Offer_table(Base):
    __tablename__ = "offers"

    offer_id: UUID = Column(UUIDP(as_uuid=True), primary_key=True)
    mentor_id: UUID = Column(UUIDP(as_uuid=True), ForeignKey('mentors.mentor_id', ondelete='CASCADE'), nullable=False)
    user_id: UUID = Column(UUIDP(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    message: str = Column(Text, nullable=True)
    status: bool = Column(Boolean, nullable=True)
    date: datetime.datetime = Column(TIMESTAMP, nullable=False)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_cache():
    redis_conn = os.getenv("REDIS_CONN")
    host, port = redis_conn.split(":")

    redis_client = redis.Redis(
        host=host,
        port=int(port),
        decode_responses=True
    )

    try:
        return redis_client
    finally:
        redis_client.close()

def init_db():
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except sqlalchemy.exc.OperationalError:
            time.sleep(1)