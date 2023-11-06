from .exceptions import AuthSaveError
from .models import Authentications as AuthModel
from ..databases import DBConnectionHandler as DBContext


def save(ctx: DBContext, auth_model: AuthModel) -> AuthModel:
    global cursor
    try:
        cursor = ctx.session
        cursor.add(auth_model)
        cursor.commit()
        cursor.refresh(auth_model)
    except Exception as error:
        cursor.rollback()
        raise AuthSaveError("Nous avons rencontré une error lors de la sauvegarde")
    else:
        return auth_model
