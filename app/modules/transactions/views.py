from flask import request, redirect, url_for, flash
from app.modules.transactions import services
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, Forbidden


def payment_callback_view():
    try:
        response_code = request.args.get("vnp_ResponseCode", None)
        txn_ref = request.args.get("vnp_TxnRef", None)
        res = services.handle_payment_callback(txn_ref=txn_ref, response_code=response_code)

        booking = res.get("booking")
        is_success = res.get("is_success")

        if is_success:
            flash("Thanh toán thành công. Đơn đặt sân của bạn đã được hệ thống ghi nhận.", "success")
        else:
            flash("Thanh toán thất bại. Giao dịch bị hủy bỏ hoặc xảy ra lỗi trong quá trình xử lý từ ngân hàng.", "danger")

        return redirect(url_for("booking.booking_detail", booking_id=booking.id))

    
    except ValidationError as e:
        return str(e.messages), 400

    except NotFound as e:
        return str(e.description), 404
    
    except Forbidden as e:
        return str(e.description), 403

    except Exception as e:
        print(e)
        flash("Có lỗi xảy ra trong quá trình xử lý thanh toán", "danger")
        return redirect(url_for("field.fields"))
