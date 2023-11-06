from datetime import datetime, timedelta
import uuid

from src import DBConnectionHandler
from src.internal.accounts import AccountController, UsernameNotFoundError
from .dependencies import is_valid_password, generate_token
from .exceptions import InvalidAccessError
from .models import Authentications as AuthModel
from .schemas import Authentication, Token
from .services import save


class AuthenticationController:

    @classmethod
    def login(cls, username: str, password: str):
        with DBConnectionHandler() as db_context:
            try:
                account_response = AccountController.find_by_email(username)
                if not is_valid_password(password, account_response.password, account_response.encrypt_key):
                    raise InvalidAccessError("Username or password is invalid, please try again")

                auth_model = AuthModel()
                auth_model.id = str(uuid.uuid4())
                auth_model.create_at = datetime.now()
                auth_model.account_id = account_response.id
                auth_model.access_token = generate_token(account_response.id, [], timedelta(minutes = 30))
                auth_model.refresh_token = generate_token(account_response.id, [], timedelta(days = 7),
                                                          is_refresh = True)

                response = save(db_context, auth_model)

            except UsernameNotFoundError as err:
                raise InvalidAccessError(err.args[0])
            except Exception as err:
                raise err
            else:
                return Authentication(
                    id = response.id,
                    username = account_response.username,
                    account_id = account_response.id,
                    user_id = account_response.user.id,
                    authorization = Token(
                        token = response.access_token,
                        refresh_token = response.refresh_token,
                        is_expired = response.is_expired
                    ),
                    create_at = account_response.create_at,
                    update_at = account_response.update_at
                )

    @classmethod
    def logout(cls):
        pass
