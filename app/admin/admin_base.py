from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.modules.auth import dao as auth_dao
from app.modules.auth.models import UserRoleEnum, UserStatusEnum

from markupsafe import Markup
from wtforms import TextAreaField
from wtforms.widgets import TextArea

import cloudinary.uploader


class AdminView(ModelView):
    page_size = 10
    can_set_page_size = True
    column_default_sort = ('id', True)
    def is_accessible(self) -> bool:
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if not user_id:
                return False
            user = auth_dao.get_user_by_id(user_id)

            return (user is not None and user.role == UserRoleEnum.ADMIN and user.status == UserStatusEnum.ACTIVE)

        except Exception:
            return False


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class', 'ckeditor5')
        html = super().__call__(field, **kwargs)
        script = Markup(f"""
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                ClassicEditor
                    .create(document.querySelector('#{field.id}'))
                    .then(editor => {{
                        editor.model.document.on('change:data', () => {{
                            document.querySelector('#{field.id}').value = editor.getData();
                        }});
                    }})
                    .catch(error => console.error(error));
            }});
        </script>
        """)
        return html + script



class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


def upload_to_cloudinary(file):
    result = cloudinary.uploader.upload(file)
    return result.get("secure_url")


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')


# class MyLogoutView(BaseView):
#     @expose('/')
#     def index(self) -> str:
#         logout_user()
#         return redirect("/admin")
#
#     def is_accessible(self) -> bool:
#         return current_user.is_authenticated


# class MyLoginView(BaseView):
#     @expose('/', methods=['GET', 'POST'])
#     def index(self):
#         err_msg = None
#
#         if request.method == 'POST':
#             tenNguoiDung = request.form.get('tenNguoiDung')
#             matKhau = request.form.get('matKhau')
#
#             tk = dao.auth_user(tenNguoiDung, matKhau)
#             if tk:
#                 login_user(tk)
#                 return redirect('/admin')
#
#             err_msg = "Tên người dùng hoặc mật khẩu không đúng"
#
#         return self.render('admin/login.html', err_msg=err_msg)
#
#     def is_accessible(self) -> bool:
#         return not current_user.is_authenticated

admin = Admin(name="SPORT BOOKING MANAGEMENT SYSTEM", theme=Bootstrap4Theme(),  index_view=MyAdminIndexView())

# admin.add_view(MyLogoutView(name="Đăng xuất"))
# admin.add_view(MyLoginView(name="Đăng nhập"))