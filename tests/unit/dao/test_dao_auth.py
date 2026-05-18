from tests.test_base import test_app, test_session
import pytest
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.modules.auth.models import User
from app.modules.auth.dao import create_new_user, check_user, get_user_by_id, update_password, update_user_info


def test_create_user(test_session):
    password = generate_password_hash("Abc@123456")
    create_new_user(password=password, username='test')
    user = User.query.filter_by(username='test').first()

    assert user.username == 'test'
    assert check_password_hash(user.password, "Abc@123456")

    with pytest.raises(IntegrityError):
        create_new_user(password=password, username='test')

    assert User.query.count() == 1


def test_check_user(test_session):
    password = generate_password_hash("Abc@123456")
    create_new_user(password=password, username='test')
    user = User.query.filter_by(username='test').first()

    assert user.username == 'test'

    user_found = check_user(username='test')
    assert user_found.username == 'test'
    assert check_password_hash(user_found.password, "Abc@123456")

    user_found = check_user(username='testtest')
    assert user_found is None


def test_get_user_by_id(test_session):
    password = generate_password_hash("Abc@123456")
    user = create_new_user(password=password, username='test')
    assert user.username == 'test'

    user_found = get_user_by_id(user.id)
    assert user_found.username == 'test'
    assert check_password_hash(user_found.password, "Abc@123456")


def test_update_password(test_session):
    password = generate_password_hash("Abc@123456")
    user = create_new_user(password=password, username='test')
    assert user.username == 'test'

    new_password = generate_password_hash("Test@123")
    user = update_password(user, new_password)
    assert user.username == 'test'
    assert check_password_hash(user.password, "Test@123")
    assert not check_password_hash(user.password, "Abc@123456")


def test_update_user_info(test_session):
    password = generate_password_hash("Abc@123456")
    create_new_user(password=password, username='test')
    user = User.query.filter_by(username='test').first()
    assert user.username == 'test'

    user = update_user_info(user, avatar="https://fake-image.png", email="123@gmail.com")
    assert user.username == 'test'
    assert user.avatar == "https://fake-image.png"
    assert user.email == "123@gmail.com"

    user2 = create_new_user(password=password, username='test2')
    with pytest.raises(ValueError, match="Email đã được đăng ký"):
        update_user_info(user2, email="123@gmail.com")

    user = update_user_info(user, email="123@gmail.com")
    assert user.username == 'test'
    assert user.email == "123@gmail.com"