import dataclasses
from datetime import datetime
from typing import Any

from src.internal.users.schemas import Users as UserEntity


@dataclasses.dataclass
class Accounts:
    id: str | None = None
    username: str | None = None
    password: Any | None = None
    encrypt_key: Any | None = None
    user: UserEntity | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "user": self.user,
            "create_at": self.create_at,
            "update_at": self.update_at
        }