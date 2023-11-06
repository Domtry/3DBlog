from sqlalchemy import select, desc

from .exceptions import UserSaveError, UserNotFoundError
from .models import Users as UserModel
from ..databases import DBConnectionHandler as DBContext


def save(ctx: DBContext, user: UserModel) -> UserModel:
    global cursor
    try:
        cursor = ctx.session
        cursor.add(user)
        cursor.commit()
        cursor.refresh(user)
    except Exception as error:
        cursor.rollback()
        raise UserSaveError("Nous avons rencontré une error lors de la sauvegarde")
    else:
        return user


def get_one(ctx: DBContext, user_id: str) -> UserModel:
    global cursor
    try:
        cursor = ctx.session
        stmt = cursor.query(UserModel).filter(
            UserModel.id == user_id
        )

        if not (db_response := cursor.execute(stmt).first()):
            raise UserNotFoundError("Nous n'avons trouvé aucun utilisateur avec cette réference")

        user_model: UserModel = db_response[0]
    except Exception as error:
        raise error
    else:
        return user_model


def paginate(ctx: DBContext, skip: int, limit: int) -> list[UserModel]:
    global cursor
    try:
        user_array: list[UserModel] = []

        cursor = ctx.session
        stmt = cursor.query(UserModel).order_by(
            desc(UserModel.create_at)).offset(skip).limit(limit)

        db_response = cursor.execute(stmt).all()
        for item in db_response:
            user_array.append(item[0])

    except Exception as error:
        raise error
    else:
        return user_array
