import logging
import os
from typing import Mapping, Any

from flask import Flask

from src.api import api_router
from src.internal.databases import DBConnectionHandler, DBConnect
from src.views import view_routing


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config = True)
    logging.basicConfig(
        filemode = '+a',
        filename = 'app.log',
        format = '[%(asctime)s]> %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('flask_cors').level = logging.DEBUG

    if test_config is None:
        app.config.from_mapping(
            FLASK_ENV = os.environ.get('FLASK_ENV'),
            FLASK_APP = os.environ.get('FLASK_APP'),
            SECRET_KEY = os.environ.get('SECRET_KEY'),
            FLASK_DEBUG = os.environ.get('FLASK_DEBUG'),

            MAX_CONTENT_LENGTH = 2 * 1024 * 1024,
            FLASK_RUN_HOST = os.environ.get('FLASK_RUN_HOST'),
            FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT'),
            JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)

    engine = DBConnectionHandler().get_engine()
    DBConnect.init_db(engine)

    view_routing(app)
    api_router(app)

    return app
