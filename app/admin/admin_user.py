from app.admin.admin_base import AdminView
from app.modules.auth.models import User, UserRoleEnum, UserStatusEnum
from sqlalchemy import func
from wtforms import SelectField
from werkzeug.security import generate_password_hash


class UserAdmin(AdminView):
    column_labels = {
        'username': 'Tên người dùng',
        'email': 'Email',
        'last_name': 'Họ',
        'first_name': 'Tên',
        'phone': 'Số điện thoại',
        'avatar': 'Avatar',
        'status': 'Trạng thái',
        'role': 'Vai trò',
        'created_at': 'Ngày tạo'
    }
    column_list = ['username', 'email', 'phone', 'first_name', 'last_name', 'role', 'status']
    column_searchable_list = ['username', 'email', 'phone']
    column_filters = ['role', 'status', 'created_at']

    column_default_sort = ('created_at', True)

    def format_date(view, context, model, name):
        return model.created_at.strftime("%d/%m/%Y %H:%M")

    column_formatters = {
        'created_at': format_date,
    }

    form_overrides = {
        'role': SelectField,
        'status': SelectField,
    }

    form_args = {
        'role': {
            'choices': [
                (UserRoleEnum.CUSTOMER.name, "Khách hàng")
            ],
            'default': UserRoleEnum.CUSTOMER.name
        },
        'status': {
            'choices': [
                (UserStatusEnum.ACTIVE.name, "Hoạt động"),
                (UserStatusEnum.BANNED.name, "Bị cấm")
            ],
            'default': UserStatusEnum.ACTIVE.name
        },
    }

    form_excluded_columns = ['password', 'avatar', 'bookings', 'reports', 'reviews', 'created_at']

    def on_form_prefill(self, form, id):
        form.username.render_kw = {'readonly': True}
        form.email.render_kw = {'readonly': True}


    def get_query(self):
        return self.session.query(self.model).filter(self.model.role == UserRoleEnum.CUSTOMER)

    def get_count_query(self):
        return self.session.query(func.count(self.model.id)).filter(self.model.role == UserRoleEnum.CUSTOMER)

    def on_model_change(self, form, model, is_created):
        if is_created:
            password = model.username + "Aa@123"
            model.password = generate_password_hash(password)

        return super().on_model_change(form, model, is_created)