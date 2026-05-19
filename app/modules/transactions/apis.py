from flask import request, jsonify
from . import services
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import Forbidden, NotFound


def payment_api():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        booking_id = int(data.get("booking_id"))
        payment_url = services.create_payment_url(booking_id=booking_id, user_id=user_id, remote_addr = request.remote_addr)

        return jsonify({"success": True, "payment_url": payment_url}), 200

    except ValidationError as e:
        return jsonify({"success": False, "message": e.messages}), 400

    except NotFound as e:
        return jsonify({"success": False, "message": e.description}), 404

    except Forbidden:
        raise

    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e), "message": "Lỗi hệ thống vui lòng thử lại sau"}), 500
