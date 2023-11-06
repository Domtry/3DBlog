import os

from apifairy import APIFairy
from flask import Flask

from src.api.endpoints.model_3d import model_3d_bp
from src.api.endpoints.users import users_bp


def api_router(app: Flask):
    app.config.from_mapping(
        APIFAIRY_VERSION = '0.0.1',
        APIFAIRY_TITLE = "3DBlog API",
        APIFAIRY_UI = os.environ.get('DOCS_UI', 'rapidoc'),
    )

    app.register_blueprint(users_bp)
    app.register_blueprint(model_3d_bp)

    APIFairy(app)