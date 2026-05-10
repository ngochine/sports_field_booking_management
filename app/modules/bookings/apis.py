from flask import request, jsonify
from . import services, schemas
from app.modules.fields import dao as field_dao
from app.common import decorators
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity


def calculate_price_api():
    data = request.get_json()

    validated_data = schemas.BookingInputTotalSchema().load(data)
    field = field_dao.get_field_by_id(int(validated_data.get("field_id")))
    validated_data.pop("field_id")
    total_price = services.caculator_total_price(field = field, **validated_data)
    total_time = services.caculator_total_time(**validated_data)

    return jsonify({
        "success": True,
        "total_time": total_time,
        "total_price": total_price
    }), 200


@decorators.login_required_api
def cancelled_booking_api(booking_id):
    try:
        data = request.get_json()
        validated_data = schemas.BookingCancelledSchema().load(data)
        user_id = get_jwt_identity()
        booking = services.cancelled_booking_service(booking_id, user_id, validated_data)

        return jsonify({
            "success": True,
            "booking": schemas.BookingOutputSchema().dump(booking)
        }), 200
    
    except ValidationError as e:
        return jsonify({"success": False, "message": e.messages}), 400
    
    except PermissionError as e:
        return jsonify({"success": False, "message": e.messages}), 403

    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e), "message": "Lỗi hệ thống vui lòng thử lại sau"}), 500
    

