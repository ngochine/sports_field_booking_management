from functools import wraps
from flask import redirect
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def login_required(f):
    @wraps(f)
    def decorated_login(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=['cookies'])
            return f(*args, **kwargs)
        except Exception:
            return redirect('/login')
    return decorated_login
