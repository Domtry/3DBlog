from typing import Any

from marshmallow import fields, Schema

from src.api.endpoints.schemas import AbstractSchema


class UserSchema(AbstractSchema):
    name = fields.String(required = True)
    pseudo = fields.String(required = True)
    email = fields.Email(required = True)
    badges = fields.List(fields.String, dump_only = True, default = [])


class ArrayUserScheme(Schema):
    users = fields.Nested(UserSchema, many = True)
    count = fields.Int(dump_only = True, default = 0)

    class Meta:
        ordered = True

    def jsonify(self, value: dict[str, Any]):
        return value
