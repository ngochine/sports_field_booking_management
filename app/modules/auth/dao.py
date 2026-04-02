from app import db
from app.modules.auth.models import User
from sqlalchemy.exc import IntegrityError

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