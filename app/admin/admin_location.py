from app.admin.admin_base import AdminView

from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired

from app.modules.bookings import dao as bookings_dao
from app.extension import db
from app.modules.fields.models import Address


class LocationAdmin(AdminView):
    form_columns = ['name', 'province_id', 'province_name', 'district_id', 'district_name', 'street', 'description']
    form_extra_fields = {
        'province_id': SelectField(
            'Tỉnh / Thành phố',
            coerce=int,
            validators=[DataRequired()],
            validate_choice=False
        ),
        'district_id': SelectField(
            'Quận / Huyện',
            coerce=int,
            validators=[DataRequired()],
            validate_choice=False
        ),

        'province_name': HiddenField(),
        'district_name': HiddenField(),
        'street': StringField(
            'Số nhà / Đường',
            validators=[DataRequired()]
        )
    }

    extra_js = ['/static/js/admin/location.js']

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.province_id.choices = [(0, "Chọn tỉnh/thành")]
        form.district_id.choices = [(0, "Chọn quận/huyện")]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        if obj and obj.address:
            address = obj.address
            form.street.data = address.street
            form.province_id.choices = [(address.province_id, address.province_name)]
            form.district_id.choices = [(address.district_id, address.district_name)]

            form.province_id.data = address.province_id
            form.district_id.data = address.district_id

            form.province_name.data = address.province_name
            form.district_name.data = address.district_name

            have_future_booking = any(
                bookings_dao.check_future_booking(field)
                for field in obj.fields
            )

            if have_future_booking:
                form.province_id.render_kw = {
                    "disabled": True
                }
                form.district_id.render_kw = {
                    "disabled": True
                }

        return form

    def on_model_change(self, form, model, is_created):
        with db.session.no_autoflush:
            if model.address:
                model.address.street = form.street.data
                model.address.province_id = form.province_id.data
                model.address.province_name = form.province_name.data
                model.address.district_id = form.district_id.data
                model.address.district_name = form.district_name.data
            else:
                address = Address(
                    street=form.street.data,
                    province_id=form.province_id.data,
                    province_name=form.province_name.data,
                    district_id=form.district_id.data,
                    district_name=form.district_name.data
                )
                model.address = address
                db.session.add(address)
                db.session.flush()
                model.address_id = address.id