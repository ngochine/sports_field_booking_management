from marshmallow import Schema, fields, ValidationError, validates_schema, validates
from datetime import date, datetime, timedelta
from .models import BookingStatusEnum
from app.modules.auth import schemas as auth_schemas
from app.modules.fields import schemas as field_schemas


class BookingInputSchema(Schema):
    booking_date= fields.Date(required=True, error_messages={"required": "Vui lòng chọn ngày đặt sân", "invalid": "Ngày đặt không hợp lệ"})
    start_time = fields.Time(required=True, error_messages={"required": "Vui lòng chọn giờ bắt đầu", "invalid": "Giờ bắt đầu không hợp lệ"})
    end_time = fields.Time(required=True, error_messages={"required": "Vui lòng chọn giờ kết thúc", "invalid": "Giờ kết thúc không hợp lệ"})

    @validates_schema
    def validate_date(self, data, **kwargs):
        if data.get("start_time") >= data.get("end_time"):
            raise ValidationError("Giờ bắt đầu phải sớm hơn giờ kết thúc")
        
        if data.get("booking_date") == date.today():
            if data.get("start_time") <= (datetime.now() + timedelta(hours=1)).time():
                raise ValidationError("Phải đặt sân trước ít nhất 1 tiếng")
            
        start = datetime.combine(data.get("booking_date"), data.get("start_time"))
        end = datetime.combine(data.get("booking_date"), data.get("end_time"))
        duration= (end - start).total_seconds() / 3600
        if duration < 1:
            raise ValidationError("Bạn cần đặt ít nhất 1 giờ")
            
    @validates("booking_date")
    def validate_booking_date(self, value, **kwargs):
        if value < date.today():
            raise ValidationError("Ngày được đặt không được ở quá khứ")
        return value
    

class BookingOutputSchema(Schema):
    id = fields.Integer()
    booking_date = fields.Date()
    start_time = fields.Time()
    end_time = fields.Time()
    status = fields.Enum(BookingStatusEnum)
    total_price = fields.Decimal()
    user = fields.Nested(auth_schemas.UserOutputBookingSchema)
    field = fields.Nested(field_schemas.FieldOutputBookingSchema)
    created_at = fields.DateTime()


class BookingInputTotalSchema(Schema):
    field_id = fields.Integer(required=True)
    booking_date = fields.Date(required=True, error_messages={"required": "Vui lòng chọn ngày đặt", "invalid": "Ngày đặt không hợp lệ"})
    start_time = fields.Time(required=True,error_messages={"required": "Vui lòng chọn giờ bắt đầu", "invalid": "Giờ bắt đầu không hợp lệ"})
    end_time = fields.Time(required=True, error_messages={"required": "Vui lòng chọn giờ kết thúc", "invalid": "Giờ kết thúc không hợp lệ"})

    @validates_schema
    def validate_date(self, data, **kwargs):
        if data.get("start_time")  >= data.get("end_time"):
            raise ValidationError("Giờ bắt đầu phải sớm hơn giờ kết thúc")


class BookingCancelledSchema(Schema):
    status = fields.Str(required=True, error_messages={"required": "Vui lòng cung cấp trạng thái"})

    @validates("status")
    def validate_status(self, value, **kwargs):
        valid_status = [e.name for e in BookingStatusEnum]

        if value not in valid_status:
            raise ValidationError("Trạng thái hủy không hợp lệ")

        return value