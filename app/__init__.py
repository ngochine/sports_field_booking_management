from flask import Flask
from app.extension import db, migrate, jwt
from instances.config import Config
import cloudinary
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.modules.auth import dao
from werkzeug.exceptions import Unauthorized
from flask import jsonify


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    cloudinary.config(
        cloud_name=flask_app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=flask_app.config['CLOUDINARY_API_KEY'],
        api_secret=flask_app.config['CLOUDINARY_API_SECRET'],
    )

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    jwt.init_app(flask_app)

    @flask_app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = dao.get_user_by_id(user_id)
                return dict(current_user=user)
        except Exception as e:
            print(e)

        return dict(current_user=None)
    
    @flask_app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({
            "success": False,
            "message": e.description
        }), 401
    
    import app.modules.auth.models
    import app.modules.fields.models
    import app.modules.bookings.models
    import app.modules.transactions.models

    from app.modules.auth.routes import auth_bp, api_auth_bp
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(api_auth_bp)

    from app.modules.fields.routes import field_bp, api_field_bp
    flask_app.register_blueprint(field_bp)
    flask_app.register_blueprint(api_field_bp)

    return flask_app