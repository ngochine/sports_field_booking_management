from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Enum as sqlEnum
from datetime import datetime
from app.extension import db
from enum import Enum

class UserRoleEnum(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class UserStatusEnum(Enum):
    ACTIVE = "active"
    BANNED = "banned"


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    avatar = Column(String(100), default='')
    status = Column(sqlEnum(UserStatusEnum), default=UserStatusEnum.ACTIVE)
    role = Column(sqlEnum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'