from flask import render_template
from . import dao
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


@decorators.login_required_render
def profile():
    current_user_id = get_jwt_identity()
    user = dao.get_user_by_id(current_user_id)

    #flash ra nữa
    
    return render_template("auth/profile.html", user=user)