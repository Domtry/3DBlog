import dataclasses
from datetime import datetime
from typing import Any

from src.internal.users.schemas import Users as UserEntity


@dataclasses.dataclass
class Token:
    token: str
    refresh_token: str
    is_expired: bool


@dataclasses.dataclass
class Authentication:
    id: str | None = None
    username: str | None = None
    account_id: str | None = None
    user_id: str | None = None
    authorization: Token | None = None
    create_at: datetime | None = None
    update_at: datetime | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "account_id": self.account_id,
            "authorization": self.authorization,
            "create_at": self.create_at,
            "update_at": self.update_at
        }