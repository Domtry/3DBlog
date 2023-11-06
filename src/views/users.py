from flask import Flask, render_template

from src.internal.users import UserController


def user_router(app: Flask):

    @app.get("/users/<int:skip>/<int:limit>")
    def welcome(skip: int, limit: int):
        response = UserController.pagination(skip, limit)
        return render_template("users/users.html", contents=response)
