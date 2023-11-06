from sqlalchemy import desc

from .exceptions import (
    AccountSaveError,
    AccountNotFoundError,
    UsernameNotFoundError)
from .models import Accounts as AccountModel
from ..databases import DBConnectionHandler as DBContext
from ..users.models import Users as UserModel


def save(ctx: DBContext, account: AccountModel) -> AccountModel:
    global cursor
    try:
        cursor = ctx.session
        cursor.add(account)
        cursor.commit()
        cursor.refresh(account)
    except Exception as error:
        cursor.rollback()
        raise AccountSaveError("Nous avons rencontré une error lors de la sauvegarde")
    else:
        return account


def get_one(ctx: DBContext, account_id: str) -> AccountModel:
    global cursor
    try:
        cursor = ctx.session
        stmt = cursor.query(AccountModel).filter(
            AccountModel.id == account_id
        )

        if not (db_response := cursor.execute(stmt).first()):
            raise AccountNotFoundError("Nous n'avons trouvé aucun compte avec cette réference")

        user_model: AccountModel = db_response[0]
    except Exception as error:
        raise error
    else:
        return user_model


def paginate(ctx: DBContext, skip: int, limit: int) -> list[AccountModel]:
    global cursor
    try:
        account_array: list[AccountModel] = []

        cursor = ctx.session
        stmt = cursor.query(AccountModel).order_by(
            desc(AccountModel.create_at)).offset(skip).limit(limit)

        db_response = cursor.execute(stmt).all()
        for item in db_response:
            account_array.append(item[0])
    except Exception as error:
        raise error
    else:
        return account_array


def search_by_email(ctx: DBContext, email: str) -> AccountModel:
    global cursor
    try:
        cursor = ctx.session
        stmt = cursor.query(AccountModel, UserModel).where(
            (AccountModel.user_id == UserModel.id) &
            (UserModel.email == email)
        )

        if not (db_response := cursor.execute(stmt).first()):
            raise UsernameNotFoundError("Nous n'avons trouvé aucun compte")

        user_model: AccountModel = db_response[0]
    except Exception as error:
        raise error
    else:
        return user_model