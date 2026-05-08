from marshmallow import Schema, fields


class FieldTypeSchema(Schema):
    id = fields.Int()
    name = fields.String()

class LocationSchema(Schema):
    id = fields.Int()
    name = fields.String()


class FieldOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    image = fields.String()
    field_type = fields.Nested(FieldTypeSchema)
    location = fields.Nested(LocationSchema)


class FieldPriceSchema(Schema):
    start_time = fields.Time()
    end_time = fields.Time()
    price = fields.Decimal()


class FieldOutputBookingSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
