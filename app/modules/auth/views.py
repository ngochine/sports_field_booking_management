from flask import render_template
from app.modules.bookings import dao as booking_dao
from app.modules.fields import dao as field_dao
from app.common import decorators
from flask_jwt_extended import get_jwt_identity


def index():
    hot_fields = field_dao.get_hot_field()
    field_types = field_dao.get_list_field_type()
    return render_template("index.html", hot_fields = hot_fields, field_types=field_types)


def register():
    return render_template('auth/register.html')


def login():
    return render_template("auth/login.html")


def profile():
    user_id = get_jwt_identity()
    bookings = booking_dao.get_bookings_by_user(user_id=user_id)
    total_bookings = len(bookings)
    return render_template("auth/profile.html", bookings=bookings[:2], total_bookings=total_bookings)


def update_profile():
    return render_template("auth/update-profile.html")