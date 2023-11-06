import dataclasses
import datetime
from typing import Any


@dataclasses.dataclass
class Users:
    id: str | None = None
    name: str | None = None
    email: str | None = None
    pseudo: str | None = None
    badges: str | None = None
    create_at: datetime.datetime | None = None
    update_at: datetime.datetime | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "pseudo": self.pseudo,
            "badges": self.badges,
            "create_at": self.create_at,
            "update_at": self.update_at
        }
