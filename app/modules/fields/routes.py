from flask import Blueprint
from . import views, apis

field_bp = Blueprint('field', __name__)

@field_bp.route('/fields', methods=['GET'])
def fields():
    return views.get_fields()




# API
api_field_bp = Blueprint('api_field', __name__, url_prefix='/api/field')

@api_field_bp.route('/fields', methods=['GET'])
def fields_api():
    return apis.get_fields_api()

