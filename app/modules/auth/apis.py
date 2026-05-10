from flask import request, jsonify
from . import schemas, services
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    get_jwt_identity, set_access_cookies, unset_jwt_cookies, set_refresh_cookies, get_jwt
from app.extension import jwt
from app.common import decorators

def register_api():
    try:
        data = request.get_json()

        validated_data = schemas.UserInputSchema().load(data)
        user = services.register_user(validated_data)

        return jsonify({
            "success": True,
            "user":  schemas.UserOutputSchema().dump(user)
        }), 201
    
    except ValidationError as e:
        return jsonify({"success": False, "message": e.messages}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Lỗi hệ thống vui lòng thử lại sau"}), 500


def login_api():
    try:
        data = request.get_json()
        validated_data = schemas.UserLoginInputSchema().load(data)

        user = services.authenticate_user(
            validated_data.get("username"),
            validated_data.get("password")
        )

        if not user:
            return jsonify({
                "success": False,
                "message": "Sai tài khoản hoặc mật khẩu"
            }), 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        resp = jsonify({
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": schemas.UserOutputSchema().dump(user)
        })

        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

    except ValidationError as e:
        return jsonify({"success": False, "message": e.messages}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Lỗi hệ thống vui lòng thử lại sau"}), 500


@jwt_required(refresh=True)
def refresh_api():
    user_id = get_jwt_identity()

    new_access_token = create_access_token(identity=user_id)
    resp = jsonify({
        "success" : True,
        "access_token": new_access_token
    })
    set_access_cookies(resp, new_access_token)

    return resp, 200


revoked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens


@decorators.login_required_api
def logout_api():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    resp = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(resp)
    return resp, 200


@decorators.login_required_api
def profile_api():
    
    if request.method == 'GET':
        pass

    elif request.method == 'PATCH':
        pass