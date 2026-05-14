from app.admin.admin_base import admin
from app.extension import db


def init_admin(app):
    admin.init_app(app)

    from app.admin.admin_field import FieldAdmin
    from app.admin.admin_field_type import FieldTypeAdmin
    from app.admin.admin_location import LocationAdmin

    from app.modules.fields.models import Field, Location, FieldType
    from app.modules.bookings.models import FieldPrice


    admin.add_view(FieldAdmin(Field, db.session, name="Quản lý sân", endpoint="admin_field"))
    admin.add_view(FieldTypeAdmin(FieldType, db.session,
                                  name="Loại sân", category="Danh mục quản lý"))

    admin.add_view(LocationAdmin(Location, db.session,
                                 name="Địa điểm", category="Danh mục quản lý"))

    # admin.add_view(LocationAdmin(Location, db.session,
    #                              name="Địa điểm", endpoint="admin_location", category="Danh mục quản lý"))