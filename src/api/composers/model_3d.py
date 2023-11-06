import uuid
from typing import Any

from flask import Request

from src.api.data import HttpResponse
from src.internal.model_3d.controllers import Model3dController
from src.internal.model_3d.schemas import Model3D as Model3DEntity
from src.internal.model_3d.exceptions import Model3dSaveError, Model3dNotFoundError
from src.internal.users import UserController


class Model3dComposer:
    @classmethod
    def save(cls, request: Request, params: dict[str, Any] | None = None) -> HttpResponse:
        global response
        try:
            body = request.json
            search_user = UserController.get_user(body["user_id"])

            model3d_entity = Model3DEntity(
                id = str(uuid.uuid4()),
                label = body["label"],
                description = body["description"],
                image_path = body["image_path"],
                user = search_user,
            )

            response = Model3dController.create_model_3d(model3d_entity)
        except Model3dSaveError as err:
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
                message = "model3D has been saved",
                success = True,
                code_status = 200
            )

    @classmethod
    def get(cls, request: Request, params: dict[str, Any] | None = None) -> HttpResponse:
        global response
        try:
            model_3d_id = params["model_3d_id"]
            response = Model3dController.get_model_3d(model_3d_id)
        except Model3dNotFoundError as err:
            return HttpResponse(
                data = None,
                message = err.args[0],
                success = False,
                code_status = 422
            )
        else:
            return HttpResponse(
                data = response.to_json(),
                message = "Model3d has been",
                success = True,
                code_status = 200
            )

    @classmethod
    def pagination(cls, request: Request, params: dict[str, Any] | None = None) -> HttpResponse:
        global response
        try:
            skip = params["skip"]
            limit = params["limit"]
            response = Model3dController.pagination(skip, limit)
        except Exception as err:
            return HttpResponse(
                data = None,
                message = err.args[0],
                success = False,
                code_status = 404
            )
        else:
            return HttpResponse(
                data = {"model3ds": response, "count": len(response)},
                message = "Données récupéré avec succès",
                success = True,
                code_status = 200
            )