import datetime
import dataclasses
from typing import Any

from src.internal.users.schemas import Users as UserModel


@dataclasses.dataclass
class Model3D:
    id: str | None = None
    label: str | None = None
    image_path: str | None = None
    description: str | None = None
    number_views: int | None = None
    user: UserModel | None = None
    create_at: datetime.datetime | None = None
    update_at: datetime.datetime | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "image_path": self.image_path,
            "description": self.description,
            "number_views": self.number_views,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "badges": self.user.badges.split(","),
            },
            "create_at": self.create_at,
            "update_at": self.update_at
        }
