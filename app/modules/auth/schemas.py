from marshmallow import Schema, fields, validate, ValidationError, validates_schema, validates
from .models import UserStatusEnum, UserRoleEnum
import re

class UserInputSchema(Schema):
    username= fields.Str(required=True, validate=validate.Length(min=3, max=30, error="Tên đăng nhập phải từ 3-30 ký tự"))
    password= fields.Str(required=True, validate=validate.Length(min=8, max=30, error="Mật khẩu phải từ 8-30 ký tự"))
    confirm= fields.Str(required=True)

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
            raise ValidationError("Mật khẩu không được chứa khoảng cách") 
        
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,30}$', value): 
            raise ValidationError("Mật khẩu phải có số, chữ thường, chữ hoa, kí tự đặc biệt (@#$%^&+=)")


class UserOutputSchema(Schema):
    id = fields.Str(dump_default="")
    username = fields.Str(dump_default="")
    email = fields.Str(dump_default="")
    first_name = fields.Str(dump_default="")
    last_name = fields.Str(dump_default="")
    avatar = fields.Str(dump_default="")
    status = fields.Enum(UserStatusEnum, by_value=True)
    role = fields.Enum(UserRoleEnum, by_value=True)
    created_at = fields.DateTime(dump_default=None)