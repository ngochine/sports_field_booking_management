import pytest
from flask import Flask
from instances.config import Config
from app.extension import db, jwt
from flask import jsonify
from werkzeug.exceptions import Unauthorized, Forbidden


def create_app():
    app_test = Flask(__name__)
    app_test.config.from_object(Config)
    app_test.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app_test.config["SECRET_KEY"] = "test-secret-key"
    app_test.config["JWT_SECRET_KEY"] = "test-secret-key"
    app_test.config["PAGE_SIZE"] = 2
    app_test.config["TESTING"] = True
    app_test.config["PROPAGATE_EXCEPTIONS"] = False

    db.init_app(app_test)
    jwt.init_app(app_test)

    from app.modules.auth.routes import api_auth_bp
    app_test.register_blueprint(api_auth_bp)

    from app.modules.fields.routes import api_field_bp
    app_test.register_blueprint(api_field_bp)

    from app.modules.bookings.routes import api_booking_bp
    app_test.register_blueprint(api_booking_bp)

    @app_test.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({
            "success": False,
            "message": e.description
        }), 401

    @app_test.errorhandler(Forbidden)
    def handle_authorize(e):
        return jsonify({
            "success": False,
            "message": e.description
        }), 403

    return app_test


@pytest.fixture
def test_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def test_session(test_app):
    yield  db.session
    db.session.rollback()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def mock_cloudinary(monkeypatch):
    def fake_upload(file):
        return {'secure_url': 'https://fake-image.png'}

    monkeypatch.setattr('cloudinary.uploader.upload', fake_upload)


@pytest.fixture
def test_auth(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )
    test_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "Abc@123456"
        }
    )
    return test_client