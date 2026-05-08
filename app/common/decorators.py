from functools import wraps
from flask import redirect
from flask_jwt_extended import verify_jwt_in_request
from werkzeug.exceptions import Unauthorized


def login_required_render(f):
    @wraps(f)
    def decorated_login_render(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=['cookies'])
            return f(*args, **kwargs)
        except Exception:
            return redirect('/login')
    return decorated_login_render


def login_required_api(f):
    @wraps(f)
    def decorated_login_api(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=['cookies'])
            return f(*args, **kwargs)
        
        except Exception:
            raise Unauthorized("Vui lòng đăng nhập để thực hiện chức năng này")
        
    return decorated_login_api
