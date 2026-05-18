from marshmallow import Schema, fields, validate, ValidationError, validates_schema, validates
from .models import UserStatusEnum, UserRoleEnum
import re


class UserInputSchema(Schema):
    username= fields.Str(required=True, validate=validate.Length(min=3, max=30, 
                            error="Tên người dùng phải từ 3-30 ký tự"),
                            error_messages={"required": "Vui lòng không để trống tên người dùng"})
    password= fields.Str(required=True, validate=validate.Length(min=8, max=30, 
                            error="Mật khẩu phải từ 8-30 ký tự"),
                            error_messages={"required": "Vui lòng không để trống mật khẩu"})
    confirm= fields.Str(required=True, error_messages={"required": "Vui lòng không để trống xác nhận"})

    @validates_schema
    def validate_confirm(self, data, **kwargs):
        if data.get("password")  != data.get("confirm"):
            raise ValidationError("Mật khẩu nhập lại không khớp")
        
    @validates("username")
    def validate_username(self, value, **kwargs):
        if " " in value:
            raise ValidationError("Tên người dùng không được chứa khoảng trắng")
        return value
    
    @validates("password")
    def validate_password(self, value, **kwargs):
        if " " in value: 
            raise ValidationError("Mật khẩu không được chứa khoảng trắng") 
        if not re.search(r'[0-9]', value):
            raise ValidationError("Mật khẩu phải chứa số")
        if not re.search(r'[a-zA-Z]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự thường")
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự hoa")
        if not re.search(r'[@#$%^&+=]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự đặc biệt")


class UserOutputSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str()
    avatar = fields.Str(dump_default="")
    status = fields.Enum(UserStatusEnum, by_value=True)
    role = fields.Enum(UserRoleEnum, by_value=True)
    created_at = fields.DateTime()


class UserLoginInputSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Vui lòng không để trống tên đăng nhập"})
    password = fields.Str(required=True, error_messages={"required": "Vui lòng không để trống mật khẩu"})


class UserOutputBookingSchema(Schema):
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


class UserUpdatePasswordInputSchema(Schema):
    current_password= fields.Str(required=True, error_messages={"required": "Vui lòng không để trống mật khẩu hiện tại"})
    new_password= fields.Str(required=True, validate=validate.Length(min=8, max=30, 
                            error="Mật khẩu mới phải từ 8-30 ký tự"),
                            error_messages={"required": "Vui lòng không để trống mật khẩu mới"})
    confirm_password= fields.Str(required=True, error_messages={"required": "Vui lòng không để trống xác nhận"})

    @validates_schema
    def validate_confirm(self, data, **kwargs):
        if data.get("new_password")  != data.get("confirm_password"):
            raise ValidationError("Mật khẩu nhập lại không khớp")
        
    @validates("new_password")
    def validate_new_password(self, value, **kwargs):
        if " " in value: 
            raise ValidationError("Mật khẩu không được chứa khoảng trắng") 
        if not re.search(r'[0-9]', value):
            raise ValidationError("Mật khẩu phải chứa số")
        if not re.search(r'[a-zA-Z]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự thường")
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự hoa")
        if not re.search(r'[@#$%^&+=]', value):
            raise ValidationError("Mật khẩu phải chứa ký tự đặc biệt")
        

class UserUpdateInputSchema(Schema):
    email = fields.Email(error_messages={"invalid": "Vui lòng nhập đúng định dạng email"})
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str(validate=validate.Length(min=10, max=10, error="Số điên thoại có chiều dài không hợp lệ"))

    @validates("phone")
    def validate_phone(self, value, **kwargs):
        if " " in value:
            raise ValidationError("Số điện thoại không được chứa khoảng trắng")
        if not re.fullmatch(r'\d+', value):
            raise ValidationError("Số điện thoại chỉ được chứa số")