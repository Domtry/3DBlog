from typing import Any
from datetime import datetime

from marshmallow import (
    Schema,
    fields)


class AbstractSchema(Schema):
    id = fields.String(dump_only = True)
    create_at = fields.DateTime(dump_only = True, default = datetime.now())
    update_at = fields.DateTime(dump_only = True)

    class Meta:
        ordered = True

    def jsonify(self, value: dict[str, Any]):
        return value
