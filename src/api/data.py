import dataclasses
from typing import Any


@dataclasses.dataclass
class HttpResponse:
    data: dict[str, Any] | None
    message: str
    success: bool
    code_status: int
