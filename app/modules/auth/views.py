from flask import render_template, redirect, url_for
from . import dao
from app.common import  decorators
from flask_jwt_extended import jwt_required, get_jwt_identity


def index():
    return render_template("index.html")


def register():
    return render_template('auth/register.html')


def login():
    return render_template("auth/login.html")


@jwt_required()
@decorators.login_required
def profile():
    # current_user_id = get_jwt_identity()
    # user = dao.get_user_by_id(current_user_id)
    return render_template("auth/profile.html", user=user)