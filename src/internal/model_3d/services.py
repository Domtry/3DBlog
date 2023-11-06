from sqlalchemy import select, desc

from .exceptions import Model3dNotFoundError, Model3dSaveError
from .models import Model3D as Model3dModel
from ..databases import DBConnectionHandler as DBContext
from ..users.models import Users as UserModel


def save(ctx: DBContext, model_3d: Model3dModel) -> Model3dModel:
    global cursor
    try:
        cursor = ctx.session
        cursor.add(model_3d)
        cursor.commit()
        cursor.refresh(model_3d)
    except Exception as error:
        cursor.rollback()
        raise Model3dSaveError("Nous avons rencontré une error lors de la sauvegarde")
    else:
        return model_3d


def get_one(ctx: DBContext, model_3d_id: str) -> Model3dModel:
    global cursor
    try:
        cursor = ctx.session
        stmt = cursor.query(Model3dModel).filter(
            Model3dModel.id == model_3d_id
        )

        if not (db_response := cursor.execute(stmt).first()):
            raise Model3dNotFoundError("Nous n'avons trouvé aucun model3D avec cette réference")

        model_3d_model: Model3dModel = db_response[0]
    except Exception as error:
        raise error
    else:
        return model_3d_model


def get_by_user_id(ctx: DBContext, user_id: str):
    global cursor
    try:
        model_3d_array: list[Model3dModel] = []

        cursor = ctx.session
        stmt = cursor.query(Model3dModel, UserModel).filter(
            (Model3dModel.user_id == UserModel.id) &
            (UserModel.id == user_id)
        )

        db_response = cursor.execute(stmt).all()
        for item in db_response:
            model_3d_array.append(item[0])

    except Exception as error:
        raise error
    else:
        return model_3d_array

def paginate(ctx: DBContext, skip: int, limit: int) -> list[Model3dModel]:
    global cursor
    try:
        model_3d_array: list[Model3dModel] = []

        cursor = ctx.session
        stmt = cursor.query(Model3dModel).order_by(
            desc(Model3dModel.create_at)).offset(skip).limit(limit)

        db_response = cursor.execute(stmt).all()
        for item in db_response:
            model_3d_array.append(item[0])

    except Exception as error:
        raise error
    else:
        return model_3d_array
