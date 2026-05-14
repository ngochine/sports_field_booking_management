from app.extension import db
from app.modules.auth.models import User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def create_new_user(password: str, **kwargs) -> User:
    try:
        user = User(password=password, **kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    
    except IntegrityError:
        db.session.rollback()
        raise
    

def check_user(username: str) -> User:
    try:
        query = User.query
        user = query.filter_by(username=username).first()
        return user
    except Exception as e:
        raise e
    

def get_user_by_id(user_id: int) -> User:
    return User.query.get(user_id)
    

def update_password(user: User, new_password: str) -> User:
    try:
        user.password = new_password
        db.session.commit()
        return user
    
    except SQLAlchemyError:
        db.session.rollback()
        raise SQLAlchemyError()
    

def update_user_info(user: User, avatar=None, **kwargs) -> User:
    try:
        if avatar:
            user.avatar = avatar

        if kwargs.get("email"):
            exist_user = User.query.filter_by(email=kwargs.get("email")).first()

            if exist_user and exist_user.id != user.id:
                raise ValueError("Email đã được đăng ký")

        for key, value in kwargs.items():
            setattr(user, key, value)

        db.session.commit()
        return user

    except Exception:
        db.session.rollback()
        raise