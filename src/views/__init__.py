from flask import Flask

from src.views.public import public_router
from src.views.users import user_router
from src.views.model_3d import model_3d_router


def view_routing(app: Flask):
    user_router(app)
    model_3d_router(app)
    public_router(app)
