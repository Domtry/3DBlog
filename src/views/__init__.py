from flask import Flask

from src.views.public import public_router
from src.views.users import user_router


def view_routing(app: Flask):
    user_router(app)
    public_router(app)
