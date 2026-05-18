from flask import request, render_template
from app.modules.transactions import services
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, Forbidden


def payment_callback_view():
    try:
        response_code = request.args.get("vnp_ResponseCode", None)
        txn_ref = request.args.get("vnp_TxnRef", None)

        # if txn_ref is None or response_code is None:
        #     raise Forbidden("Bạn không có quyền truy cập")
        
        res = services.handle_payment_callback(txn_ref=txn_ref, response_code=response_code)

        booking = res.get("booking")
        is_success = res.get("is_success")

        return render_template("bookings/booking-details.html", booking= booking, is_success= is_success)
    
    except ValidationError as e:
        return str(e.messages), 400

    except NotFound as e:
        return str(e.description), 404
    
    except Forbidden as e:
        return str(e.description), 403

    except Exception as e:
        print(str(e)), 500
