from app.admin.admin_base import admin
from app.extension import db


def init_admin(app):
    admin.init_app(app)

    from app.admin.admin_field import FieldAdmin
    from app.admin.admin_field_type import FieldTypeAdmin
    from app.admin.admin_location import LocationAdmin
    from app.admin.admin_field_price import FieldPriceAdmin
    from app.admin.admin_user import UserAdmin

    from app.modules.fields.models import Field, Location, FieldType
    from app.modules.bookings.models import FieldPrice
    from app.modules.auth.models import User


    admin.add_view(UserAdmin(User, db.session, name="Quản lý khách hàng"))

    admin.add_view(FieldAdmin(Field, db.session, name="Quản lý sân", endpoint="admin_field"))

    admin.add_view(FieldTypeAdmin(FieldType, db.session,
                                  name="Quản lý loại sân", category="Danh mục quản lý"))

    admin.add_view(LocationAdmin(Location, db.session,
                                 name="Quản lý địa điểm", category="Danh mục quản lý"))

    admin.add_view(FieldPriceAdmin(FieldPrice, db.session,
                                 name="Quản lý giá sân", category="Danh mục quản lý"))