from .models import Users as UserModel
from ..databases import DBConnectionHandler as DBContext


def is_valid_user(ctx: DBContext, user_id: str) -> bool:
    cursor = ctx.session
    stmt = cursor.query(UserModel).filter(UserModel.id == user_id)
    stmt = cursor.query(stmt.exists())

    if not (cursor.execute(stmt).first()):
        return False
    return False
