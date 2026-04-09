from . import services, schemas
from flask import request, jsonify

# def get_field_api():
#     filters = request.args
#     fields = services.get_list_field(filters)

#     return jsonify(schemas.FieldOutputSchema(many=True).dump(fields)), 200
