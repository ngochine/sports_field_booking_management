from flask import Flask
from app.extension import db, migrate, jwt
from app.settings import Config
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

    import app.modules.auth.models
    import app.modules.fields.models
    import app.modules.bookings.models
    import app.modules.transactions.models

    return flask_app