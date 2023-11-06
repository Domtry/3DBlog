import uuid
import datetime

from sqlalchemy import (
    Column,
    DateTime,
    String
)


class AbstractModel:
    id = Column(String(170), primary_key = True, default = str(uuid.uuid4()))
    create_at = Column(DateTime, default = datetime.datetime.now())
    update_at = Column(DateTime, nullable = True)
