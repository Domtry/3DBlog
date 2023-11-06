from typing import Any

from marshmallow import fields, Schema

from src.api.endpoints.schemas import AbstractSchema


class Model3dSchema(AbstractSchema):
    label = fields.String(required = True)
    image_path = fields.URL(required = True)
    description = fields.String(required = False, default = "")
    number_views = fields.Int(required = True, dump_only = True, default = 0)
    user_id = fields.String(required = True, load_only = True)


class ArrayModel3dSchema(Schema):
    model3ds = fields.Nested(Model3dSchema, many = True)
    count = fields.Int(dump_only = True, default = 0)

    class Meta:
        ordered = True

    def jsonify(self, value: dict[str, Any]):
        return value
