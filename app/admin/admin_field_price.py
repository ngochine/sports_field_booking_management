from app.admin.admin_base import AdminView
from wtforms import ValidationError
from datetime import date
from app.modules.bookings.models import FieldPrice


class FieldPriceAdmin(AdminView):
    column_labels = {
        'field': 'Sân',
        'start_time': 'Giờ bắt đầu',
        'end_time': 'Giờ kết thúc',
        'price': 'Giá (VND)',
        'day_of_week': 'Thứ trong tuần',
        'special_date': 'Ngày đặc biệt'
    }

    column_list = ['field', 'start_time', 'end_time', 'price', 'day_of_week', 'special_date']
    column_searchable_list = ['field.name']
    column_filters = ['field.id', 'day_of_week', 'special_date']

    @staticmethod
    def format_price(view, context, model, name):
        if model.price is None:
            return "0 VND"
        return f"{model.price:,.0f} VND"

    @staticmethod
    def format_day(view, context, model, name):
        if model.day_of_week is None:
            return "-"
        days = {
            0: "Chủ nhật",
            1: "Thứ 2",
            2: "Thứ 3",
            3: "Thứ 4",
            4: "Thứ 5",
            5: "Thứ 6",
            6: "Thứ 7",
        }
        return days.get(model.day_of_week, str(model.day_of_week))

    column_formatters = {
        'price': format_price,
        'day_of_week': format_day
    }
    column_default_sort = ('field.id', False)

    def on_model_change(self, form, model, is_created):
        if model.start_time and model.end_time:
            if model.start_time >= model.end_time:
                raise ValidationError("Giờ bắt đầu phải nhỏ hơn giờ kết thúc")

        if model.special_date:
            if model.special_date < date.today():
                raise ValidationError("Không được tạo ngày đặc biệt trong quá khứ")

        query = FieldPrice.query.filter(
            FieldPrice.field_id == model.field_id,
            FieldPrice.start_time < model.end_time,
            model.start_time < FieldPrice.end_time,
        )

        if model.special_date:
            query = query.filter(FieldPrice.special_date == model.special_date)
        else:
            query = query.filter(
                FieldPrice.day_of_week == model.day_of_week,
                FieldPrice.special_date.is_(None)
            )

        if model.id:
            query = query.filter(FieldPrice.id != model.id)

        if query.first():
            raise ValidationError("Khung giờ này đã tồn tại trong bảng giá")

        return super().on_model_change(form, model, is_created)