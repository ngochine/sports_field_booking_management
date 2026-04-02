from .models import User
from . import dao
from werkzeug.security import generate_password_hash, check_password_hash
import re
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

def register_user(validate_data: dict) -> User:
    validate_data.pop('confirm', None)

    password = validate_data.pop('password')
    password = generate_password_hash(password)

    validate_data['avatar'] = "https://res.cloudinary.com/dvfuzolim/image/upload/v1768406079/avatar_trang_1_cd729c335b_kitzwg.jpg"

    try:
        return dao.create_new_user(password=password, **validate_data)
    
    except IntegrityError:
        raise ValidationError("Tên người dùng đã tồn tại")


def authenticate_user(username: str, password: str) -> User:
    try:
        user = dao.check_user(username=username)

        if user and check_password_hash(user.password, password):
            return user
        
        return None
    except Exception as e:
        raise e
