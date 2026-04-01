from app.extension import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class FieldType(db.Model):
    __tablename__ = 'field_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    def __str__(self):
        return self.name


class Address(db.Model):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    description = Column(String(255))


class Location(db.Model):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False, unique=True)
    address = relationship(Address, backref="location", uselist=False)

    def __str__(self):
        return self.name


class Field(db.Model):
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    field_type_id = Column(Integer, ForeignKey('field_type.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)

    field_type = relationship('FieldType', backref='fields')
    location = relationship('Location', backref='fields', lazy='True')

    def __str__(self):
        return f'{self.name}'


class Review(db.Model):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    field = relationship('Field', backref='reviews')
    user = relationship('User', backref='reviews')