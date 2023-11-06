import os
from typing import Any
# from pipes import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine


class DBConnectionHandler:

    def __init__(self):
        db_uri: str = ""
        self.session: Session
        if os.environ.get('FLASK_ENV') == 'production':
            db_uri: str = str(os.environ.get('SQLALCHEMY_DATABASE_URI'))
        else:
            db_uri = 'sqlite:///db_test.db'
        self.__connection_string = db_uri

    def get_engine(self):
        try:
            return create_engine(self.__connection_string)
        except Exception as err:
            print(err)

    def __enter__(self):
        try:
            engine: Engine = create_engine(self.__connection_string)
            session_maker: sessionmaker = sessionmaker()
            self.session = session_maker(bind = engine)
        except Exception as err:
            print(err)
        else:
            return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.session.close()
