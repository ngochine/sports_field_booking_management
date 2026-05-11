from marshmallow import Schema, fields, ValidationError, validates_schema, validates
from datetime import date, datetime
from .models import BookingStatusEnum
from app.modules.auth import schemas as auth_schemas
from app.modules.fields import schemas as field_schemas


class BookingInputSchema(Schema):
    booking_date= fields.Date(required=True, error_messages={"required": "Vui lòng chọn ngày đặt sân", "invalid": "Ngày đặt không hợp lệ"})
    start_time = fields.Time(required=True, error_messages={"required": "Vui lòng chọn giờ bắt đầu", "invalid": "Giờ bắt đầu không hợp lệ"})
    end_time = fields.Time(required=True, error_messages={"required": "Vui lòng chọn giờ kết thúc", "invalid": "Giờ kết thúc không hợp lệ"})

    @validates_schema
    def validate_date(self, data, **kwargs):
        if data.get("start_time")  >= data.get("end_time"):
            raise ValidationError("Giờ bắt đầu phải sớm hơn giờ kết thúc")
        
        if data.get("booking_date") == date.today():
            if data.get("start_time") <= datetime.now().time():
                raise ValidationError("Giờ bắt đầu phải lớn hơn thời gian hiện tại")
            
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
    status = fields.Enum(BookingStatusEnum)

    @validates("status")
    def validate_status(self, value, **kwargs):
        if value != BookingStatusEnum.CANCELLED:
            raise ValidationError("Trạng thái huỷ không hợp lệ")
        return value