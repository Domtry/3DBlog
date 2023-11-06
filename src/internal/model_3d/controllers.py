import datetime
import uuid
from typing import Any

from src.internal.databases import DBConnectionHandler
from .services import (
    save, get_one, paginate, get_by_user_id)
from src.internal.users import services as UserService

from .models import Model3D as Model3DModel
from .schemas import Model3D as Model3DEntity


class Model3dController:

    @classmethod
    def create_model_3d(cls, model_3d: Model3DEntity) -> Model3DEntity:
        with DBConnectionHandler() as db_context:
            try:
                model_3d_model = Model3DModel()
                model_3d_model.id = model_3d.id
                model_3d_model.label = model_3d.label
                model_3d_model.image_path = model_3d.image_path
                model_3d_model.description = model_3d.description
                model_3d_model.number_views = model_3d.number_views
                model_3d_model.user_id = model_3d.user.id
                model_3d_model.create_at = datetime.datetime.now()

                response = save(db_context, model_3d_model)

                user_model_3d = get_by_user_id(db_context, model_3d_model.user_id)
                number_model_3d = len(user_model_3d)

                if number_model_3d >= 5:
                    user = UserService.get_one(db_context, model_3d_model.user_id)
                    badges = user.badges.split()

                    if "Collector" != badges:
                        badges.append("Collector")
                        user.badges = ",".join(badges)
                        UserService.save(db_context, user)
                        model_3d.user.badges = user.badges

            except Exception as error:
                raise error
            else:
                return Model3DEntity(
                    id = response.id,
                    label = response.label,
                    image_path = response.image_path,
                    description = response.description,
                    number_views = response.number_views,
                    user = model_3d.user,
                    create_at = response.create_at,
                    update_at = response.update_at
                )

    @classmethod
    def get_model_3d(cls, model_3d_id: str) -> Model3DEntity:
        with DBConnectionHandler() as db_context:
            try:
                search_model_3d = get_one(db_context, model_3d_id)

                search_model_3d.number_views = int(search_model_3d.number_views + 1)
                if search_model_3d.number_views == 1000:
                    user = UserService.get_one(db_context, search_model_3d.user_id)
                    badges = user.badges.split()
                    if "Star" != badges:
                        badges.append("Star")
                        user.badges = ",".join(badges)
                        UserService.save(db_context, user)

                save(db_context, search_model_3d)

                user = UserService.get_one(db_context, search_model_3d.user_id)

            except Exception as err:
                raise err
            else:
                return Model3DEntity(
                    id = search_model_3d.id,
                    label = search_model_3d.label,
                    user = user,
                    description = search_model_3d.description,
                    number_views = search_model_3d.number_views,
                    image_path = search_model_3d.image_path,
                    create_at = search_model_3d.create_at,
                    update_at = search_model_3d.update_at
                )

    @classmethod
    def pagination(cls, skip, limit) -> list[dict[str, Any]]:
        with DBConnectionHandler() as db_context:
            try:
                response = paginate(db_context, skip, limit)
            except Exception as err:
                raise err
            else:
                model_3ds: list[dict[str, Any]] = []
                for model_3d in response:
                    user = UserService.get_one(db_context, model_3d.user_id)
                    current = Model3DEntity(
                        id = model_3d.id,
                        label = model_3d.label,
                        description = model_3d.description,
                        number_views = model_3d.number_views,
                        user = user,
                        create_at = model_3d.create_at,
                        update_at = model_3d.update_at
                    )
                    model_3ds.append(current.to_json())

                return model_3ds

    @classmethod
    def update(cls, model_3d_id: str, model_3d: Model3DEntity) -> Model3DEntity:
        with DBConnectionHandler() as db_context:
            try:
                search_model_3d = get_one(db_context, model_3d_id)
                if search_model_3d.label != model_3d.label:
                    search_model_3d.label = model_3d.label

                if search_model_3d.description != model_3d.description:
                    search_model_3d.description = model_3d.description

                if search_model_3d.image_path != model_3d.image_path:
                    search_model_3d.image_path = model_3d.image_path

                if search_model_3d.number_views != model_3d.number_views:
                    search_model_3d.number_views = model_3d.number_views

                response = save(search_model_3d)
                user = UserService.get_one(db_context, response.user_id)

            except Exception as err:
                raise err
            else:
                return Model3DEntity(
                    id = response.id,
                    label = response.label,
                    user = user,
                    description = response.description,
                    number_views = response.number_views,
                    image_path = response.image_path,
                    create_at = response.create_at,
                    update_at = response.update_at
                )

    @classmethod
    def get_model_3d_user_id(cls, user_id: str) -> list[dict[str, Any]]:
        with DBConnectionHandler() as db_context:
            try:
                response = get_by_user_id(db_context, user_id)
            except Exception as err:
                raise err
            else:
                model_3ds: list[dict[str, Any]] = []
                for model_3d in response:
                    user = UserService.get_one(db_context, model_3d.user_id)
                    current = Model3DEntity(
                        id = model_3d.id,
                        label = model_3d.label,
                        description = model_3d.description,
                        number_views = model_3d.number_views,
                        user = user,
                        create_at = model_3d.create_at,
                        update_at = model_3d.update_at
                    )
                    model_3ds.append(current.to_json())

                return model_3ds
