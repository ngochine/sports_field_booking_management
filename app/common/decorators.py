from functools import wraps
from flask import redirect
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.exceptions import Unauthorized, Forbidden
from flask_jwt_extended.exceptions import JWTExtendedException
from app.modules.auth.models import User, UserStatusEnum, UserRoleEnum
from jwt import ExpiredSignatureError


def login_required_render(f):
    @wraps(f)
    def decorated_login_render(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=['cookies'])
            return f(*args, **kwargs)
        except Exception as e:
            return redirect('/login')
    return decorated_login_render

def customer_required_render(f):
    @wraps(f)
    @login_required_render
    def decorated_customer_render(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.status == UserStatusEnum.BANNED:
            return redirect('/')

        if user.role != UserRoleEnum.CUSTOMER:
            return redirect('/admin')

        return f(*args, **kwargs)

    return decorated_customer_render


def login_required_api(f):
    @wraps(f)
    def decorated_login_api(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=['cookies'])
            return f(*args, **kwargs)

        except ExpiredSignatureError as e:
            raise Unauthorized("Vui lòng đăng nhập để thực hiện chức năng này")

        except JWTExtendedException as e:
            raise Unauthorized("Vui lòng đăng nhập để thực hiện chức năng này")
        
    return decorated_login_api


def customer_required_api(f):
    @wraps(f)
    @login_required_api
    def decorated_customer_api(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.status == UserStatusEnum.BANNED:
            raise Forbidden("Tài khoản của bạn bị cấm nên không thể thực hiện hành động này")

        if user.role != UserRoleEnum.CUSTOMER:
            raise Forbidden("Tài khoản của bạn không đủ quyền để thực hiện hành động này")

        return f(*args, **kwargs)

    return decorated_customer_api