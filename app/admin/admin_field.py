from app.admin.admin_base import AdminView, CKTextAreaField, upload_to_cloudinary
from markupsafe import Markup
from wtforms import FileField
from app.modules.fields.models import Field, FieldStatusEnum
from app.modules.bookings import dao as bookings_dao
from flask import flash
from sqlalchemy import func
from wtforms import StringField
from wtforms.validators import DataRequired


class FieldAdmin(AdminView):
    column_labels = {
        'name': 'Tên sân',
        'description': 'Mô tả',
        'image': 'Ảnh sân',
        'status': 'Trạng thái',
        'location': 'Địa điểm',
        'field_type': 'Loại sân'
    }
    column_list = ['name', 'field_type', 'location', 'status', 'image']
    column_searchable_list = ['name']
    column_filters = ['field_type', 'location', 'status']

    form_columns = ['name', 'field_type', 'location', 'image', 'description']

    def image_thumbnail(view, context, model, name):
        if model.image:
            return Markup(
                f'<img src="{model.image}" style="height:80px;width: 80px; border-radius:8px;">'
            )
        return ''

    column_formatters = {
        'image': image_thumbnail
    }

    extra_js = [
        'https://cdn.ckeditor.com/ckeditor5/41.4.2/classic/ckeditor.js'
    ]
    form_overrides = {
        'description': CKTextAreaField
    }

    form_extra_fields = {
        'image': FileField('Ảnh sân (Chọn ảnh từ máy)'),
        'name': StringField(
            'Tên sân',
            validators=[DataRequired()]
        )
    }

    def get_query(self):
        return super().get_query().order_by(Field.status)

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if obj and obj.image:
            form.image_preview = Markup(f"""
                <div style="margin-bottom:10px;">
                    <label>Ảnh hiện tại:</label><br>
                    <img src="{obj.image}"
                         style="width:150px;height:150px;object-fit:cover;border-radius:8px;">
                </div>
            """)
        return form

    def validate_form(self, form):
        if not super().validate_form(form):
            return False

        if not hasattr(form, 'name'):
            return True

        field_name = form.name.data.strip()
        query = Field.query.filter(func.trim(Field.name) == field_name, Field.status!= FieldStatusEnum.DELETED)

        if form._obj and form._obj.id:
            query = query.filter(Field.id != form._obj.id)

        if query.first():
            form.name.errors = ["Tên sân đã tồn tại, vui lòng đặt tên sân khác"]
            return False

        return True

    def on_model_change(self, form, model, is_created):
        file_data = form.image.data
        if file_data:
            url = upload_to_cloudinary(file_data)
            model.image = url

    deleted_message = "Xoá sân thành công"
    def delete_model(self, model):
        try:
            if bookings_dao.check_future_booking(model):
                flash("Sân đang có lịch hẹn trong tương lai, không thể xoá", "error")
                return False
            model.status = FieldStatusEnum.DELETED
            self.session.commit()
            return True

        except Exception as e:
            print(e)
            self.session.rollback()
            flash("Có lỗi xảy ra khi xoá sân", "error")

            return False

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if obj and bookings_dao.check_future_booking(obj):
            form.location.render_kw = {
                "disabled": True
            }
            form.field_type.render_kw = {
                "disabled": True
            }
        return form