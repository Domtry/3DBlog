import uuid
from cryptography.fernet import Fernet

from flask import Flask

from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBConnect:
    @classmethod
    def init_db(cls, engine: Engine, app: Flask | None = None):
        from src.internal.users.models import Users
        from src.internal.model_3d.models import Model3D
        from src.internal.authentications.models import Authentications
        from src.internal.accounts.models import Accounts

        Base.metadata.create_all(bind = engine, checkfirst = True)
