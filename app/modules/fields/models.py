from app.extension import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as sqlEnum


class FieldStatusEnum(Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class FieldType(db.Model):
    __tablename__ = 'field_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    def __str__(self):
        return self.name


class Address(db.Model):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)

    province_id = Column(Integer, nullable=False)
    province_name = Column(String(100), nullable=False)

    district_id = Column(Integer, nullable=False)
    district_name = Column(String(100), nullable=False)

    street = Column(String(255), nullable=False)

    def __str__(self):
        return f'{self.street}, {self.district_name}, {self.province_name}'


class Location(db.Model):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
    address = relationship(Address, backref="location", uselist=False)
    description = Column(String(255))

    def __str__(self):
        return self.name


class Field(db.Model):
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    image = Column(String(300))
    description = Column(Text, nullable=True)
    status = Column(sqlEnum(FieldStatusEnum), nullable=False, default=FieldStatusEnum.ACTIVE)

    field_type_id = Column(Integer, ForeignKey('field_type.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)

    field_type = relationship('FieldType', backref='fields')
    location = relationship('Location', backref='fields', lazy=True)

    def __str__(self):
        return f'{self.name}'


class Review(db.Model):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    customer_id = Column(String(50), ForeignKey('user.id'), nullable=False)

    field = relationship('Field', backref='reviews')
    user = relationship('User', backref='reviews')