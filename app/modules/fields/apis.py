from . import services, schemas
from flask import request, jsonify
from datetime import datetime
from app.modules.bookings import schemas as booking_schema
from app.modules.bookings import services as booking_service
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from app.common import decorators
from werkzeug.exceptions import NotFound


def get_field_price_api(field_id):
    try:
        date_selected = request.args.get('date', None)

        if not date_selected:
            return jsonify({'success': False, 'message': 'Thiếu ngày để tìm kiếm'}), 400

        if isinstance(date_selected, str):
            date_selected = datetime.strptime(date_selected,"%Y-%m-%d").date()

        field_prices = services.get_field_prices_service(
            field_id=field_id,
            date_selected=date_selected
        )

    except ValueError:
        return jsonify({'success': False, 'message': 'Vui lòng nhập đúng định dạng YYYY-MM-DD'}), 400

    except ValidationError as e:
        return jsonify({"success": False, "message": e.messages}), 400

    except NotFound as e:
        return jsonify({"success": False, "message": str(e.description)}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    return jsonify({
        "success": True,
        "field_prices": schemas.FieldPriceSchema(many=True).dump(field_prices)
    }), 200



def create_booking_api(field_id):
    try: 
        data = request.get_json()
        validated_data = booking_schema.BookingInputSchema().load(data)
        user_id = get_jwt_identity()
        booking = booking_service.create_booking_service(field_id= field_id, user_id= user_id, data= validated_data)

        return jsonify({
            "success": True,
            "booking": booking_schema.BookingOutputSchema().dump(booking)
        }), 201
    
    except ValidationError as e:
        return jsonify({"success": False, "message": e.messages}), 400

    except NotFound as e:
        return jsonify({"success": False, "message": str(e)}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Lỗi hệ thống vui lòng thử lại sau"}), 500