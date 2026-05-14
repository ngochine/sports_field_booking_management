from flask import Blueprint
from . import views, apis
from app.common import decorators

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    return views.index()


@auth_bp.route('/register', methods=['GET'])
def register():
    return views.register()


@auth_bp.route('/login', methods=['GET'])
def login():
    return views.login()


@auth_bp.route('/profile', methods=['GET'])
@decorators.login_required_render
def profile():
    return views.profile()


@auth_bp.route('/profile/update', methods=['GET'])
@decorators.login_required_render
def update_profile():
    return views.update_profile()



# API
api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')

@api_auth_bp.route('/register', methods=['POST'])
def register_api():
    return apis.register_api()

@api_auth_bp.route('/login', methods=['POST'])
def login_api():
    return apis.login_api()

@api_auth_bp.route('/refresh', methods=['POST'])
def refresh_token_api():
    return apis.refresh_api()


@api_auth_bp.route('/logout', methods=['POST'])
@decorators.login_required_api
def logout_api():
    return apis.logout_api()


@api_auth_bp.route('/current-user/profile', methods=['PATCH'])
@decorators.login_required_api
def profile_api():
    return apis.profile_api()


@api_auth_bp.route('/current-user/change-password', methods=['PATCH'])
@decorators.login_required_api
def user_passwrord_api():
    return apis.change_password_api()