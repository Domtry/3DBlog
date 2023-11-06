import uuid
from datetime import datetime

from cryptography.fernet import Fernet

from src import DBConnectionHandler
from src.internal.accounts.models import Accounts as AccountModel
from src.internal.accounts.schemas import Accounts as AccountEntity
from .services import (
    save,
    search_by_email)
from ..users import UserController


class AccountController:

    @classmethod
    def create_account(cls, account: AccountEntity) -> AccountEntity:
        with DBConnectionHandler() as db_context:
            try:
                encrypt_key = Fernet.generate_key()
                fernet = Fernet(encrypt_key)
                encrypt_password = fernet.encrypt(
                    account.password.encode(encoding = "UTF-8", errors = 'strict'))

                account_model = AccountModel()
                account_model.id = str(uuid.uuid4())
                account_model.username = account.username
                account_model.password = encrypt_password
                account_model.encrypt_key = encrypt_key
                account_model.user_id = account.user.id
                account_model.create_at = datetime.now()

                response = save(db_context, account_model)
            except Exception as error:
                raise error
            else:
                return AccountEntity(
                    id = response.id,
                    username = response.username,
                    user = account.user,
                    create_at = response.create_at,
                    update_at = response.update_at
                )

    @classmethod
    def find_by_email(cls, email: str) -> AccountEntity:
        with DBConnectionHandler() as db_context:
            try:
                account_response = search_by_email(db_context, email)
                user_response = UserController.get_user(account_response.user_id)
            except Exception as error:
                raise error
            else:
                return AccountEntity(
                    id = account_response.id,
                    username = account_response.username,
                    user = user_response,
                    password = account_response.password,
                    encrypt_key = account_response.encrypt_key,
                    create_at = account_response.create_at,
                    update_at = account_response.update_at
                )