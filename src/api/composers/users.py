import uuid
from typing import Any

from flask import Request

from src.api.data import HttpResponse
from src.internal.users import (
    UserController,
    UserEntity,
    UserSaveError, UserNotFoundError
)


class UserComposer:

    @classmethod
    def save(cls, request: Request, params: dict[str, Any] | None = None) -> HttpResponse:
        global response
        try:
            body = request.json
            user_entity = UserEntity(
                id = str(uuid.uuid4()),
                email = body["email"],
                name = body["name"],
                pseudo = body["pseudo"]
            )

            response = UserController.create_user(user_entity)
        except UserSaveError as err:
            return HttpResponse(
                data = None,
                message = err.args[0],
                success = False,
                code_status = 422
            )
        except Exception as err:
            return HttpResponse(
                data = None,
                message = err.args[0],
                success = False,
                code_status = 404
            )
        else:
            return HttpResponse(
                data = response.to_json(),
                message = "User has been saved",
                success = True,
                code_status = 200
            )

    @classmethod
    def get(cls, request: Request, params: dict[str, Any] | None = None) -> HttpResponse:
        global response
        try:
            user_id = params["user_id"]
            response = UserController.get_user(user_id)
        except UserNotFoundError as err:
            return HttpResponse(
                data = None,
                message = err.args[0],
                success = False,
                code_status = 422
            )
        else:
            return HttpResponse(
                data = response.to_json(),
                message = "User has been saved",
                success = True,
                code_status = 200
            )

    @classmethod
    def pagination(cls, request: Request, params: dict[str, Any] | None = None) -> HttpResponse:
        global response
        try:
            skip = params["skip"]
            limit = params["limit"]
            response = UserController.pagination(skip, limit)
        except Exception as err:
            return HttpResponse(
                data = None,
                message = err.args[0],
                success = False,
                code_status = 404
            )
        else:
            return HttpResponse(
                data = {"users": response, "count": len(response)},
                message = "User has been saved",
                success = True,
                code_status = 200
            )
