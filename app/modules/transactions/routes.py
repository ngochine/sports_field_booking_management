from flask import Blueprint
from . import views, apis
from app.common import decorators


transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/transaction/payment_return", methods=["GET"])
def payment_return():
    return views.payment_callback_view()


api_transaction_bp = Blueprint('transaction_api', __name__, url_prefix='/api')

@api_transaction_bp.route("/transaction/pay", methods=["POST"])
@decorators.customer_required_api
def pay():
    return apis.payment_api()