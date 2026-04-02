from flask import Flask
from app.extension import db, migrate, jwt
from instance.config import Config
import cloudinary

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