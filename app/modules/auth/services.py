from .models import User
from . import dao
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import NotFound
import cloudinary
import cloudinary.uploader


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
    

def update_password_service(data: dict, user_id: str):
    try:
        user = dao.get_user_by_id(user_id=user_id)
        if not user:
            raise NotFound("Không tồn tại người dùng")

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if check_password_hash(user.password, current_password):
            new_password = generate_password_hash(new_password)
            user = dao.update_password(user= user, new_password = new_password)
            return user
        else:
            raise ValidationError("Mật khẩu hiện tại không đúng")
        
    except SQLAlchemyError:
        raise Exception
    

def update_user_info_service(data: dict, user_id: str, avatar=None):
    user = dao.get_user_by_id(user_id=user_id)
    if not user:
        raise NotFound("Không tồn tại người dùng")
    if avatar:
        result = cloudinary.uploader.upload(avatar)
        avatar = result["secure_url"]

    user = dao.update_user_info(user= user, avatar=avatar, **data)
    return user