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


class Province(db.Model):
    __tablename__ = "province"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class District(db.Model):
    __tablename__ = "district"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    province_id = Column(Integer, ForeignKey("province.id"))
    province = relationship("Province", backref="districts")


class Address(db.Model):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)

    street = Column(String(255))
    district_id = Column(Integer, ForeignKey("district.id"))
    district = relationship("District")


class Location(db.Model):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False, unique=True)
    address = relationship(Address, backref="location", uselist=False)
    description = Column(String(255))
    def __str__(self):
        return self.name


class Field(db.Model):
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    image = Column(String(300))
    description = Column(Text, nullable=True)
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