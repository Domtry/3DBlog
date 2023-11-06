import uuid
import datetime
from typing import Any

from src.internal.databases import DBConnectionHandler
from .services import (save, get_one, paginate)
from .models import Users as UserModel
from .schemas import Users as UserEntity


class UserController:

    @classmethod
    def create_user(cls, user: UserEntity) -> UserEntity:
        with DBConnectionHandler() as db_context:
            try:
                user_model = UserModel()
                user_model.id = user.id
                user_model.name = user.name
                user_model.email = user.email
                user_model.pseudo = user.pseudo
                user_model.create_at = datetime.datetime.now()

                response = save(db_context, user_model)

            except Exception as error:
                raise error
            else:
                return UserEntity(
                    id = response.id,
                    name = response.name,
                    pseudo = response.pseudo,
                    email = response.email,
                    badges = response.badges,
                    create_at = response.create_at,
                    update_at = response.update_at
                )

    @classmethod
    def get_user(cls, user_id) -> UserEntity:
        with DBConnectionHandler() as db_context:
            try:
                response = get_one(db_context, user_id)
            except Exception as err:
                raise err
            else:
                return UserEntity(
                    id = response.id,
                    name = response.name,
                    pseudo = response.pseudo,
                    email = response.email,
                    badges = response.badges,
                    create_at = response.create_at,
                    update_at = response.update_at
                )

    @classmethod
    def pagination(cls, skip: int, limit: int) -> list[UserEntity]:
        with DBConnectionHandler() as db_context:
            try:
                response = paginate(db_context, skip, limit)
            except Exception as err:
                raise err
            else:
                users: list[dict[str, Any]] = []
                for user in response:
                    current = UserEntity(
                        id = user.id,
                        name = user.name,
                        pseudo = user.pseudo,
                        email = user.email,
                        badges = user.badges,
                        create_at = user.create_at,
                        update_at = user.update_at
                    )
                    users.append(current.to_json())

                return users

    @classmethod
    def update(cls, user_id: str, user: UserEntity) -> UserEntity:
        with DBConnectionHandler() as db_context:
            try:
                search_user = get_one(db_context, user_id)
                if search_user.name != user.name:
                    search_user.name = user.name

                if search_user.email != user.email:
                    search_user.email = user.email

                if search_user.pseudo != user.pseudo:
                    search_user.pseudo = user.pseudo

                if search_user.badges != user.badges:
                    search_user.badges = user.badges

                response = save(search_user)
            except Exception as error:
                raise error
            else:
                return UserEntity(
                    id = response.id,
                    name = response.name,
                    pseudo = response.pseudo,
                    email = response.email,
                    badges = response.badges,
                    create_at = response.create_at,
                    update_at = response.update_at
                )
