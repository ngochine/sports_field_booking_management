from sqlalchemy import Column, String, DateTime
from sqlalchemy import Enum as sqlEnum
from datetime import datetime
from app.extension import db
from enum import Enum
from uuid import uuid4


class UserRoleEnum(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class UserStatusEnum(Enum):
    ACTIVE = "active"
    BANNED = "banned"


class User(db.Model):
    __tablename__ = 'user'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    avatar = Column(String(100), default='')
    phone = Column(String(10), nullable=True)
    status = Column(sqlEnum(UserStatusEnum), default=UserStatusEnum.ACTIVE)
    role = Column(sqlEnum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'