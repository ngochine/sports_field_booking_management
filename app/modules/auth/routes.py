from flask import Blueprint
from . import views, apis

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
def profile():
    return views.profile()



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
def logout_api():
    return apis.logout_api()

@api_auth_bp.route('/profile', methods=['GET', 'PATCH'])
def profile_api():
    return apis.profile_api()
