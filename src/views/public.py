from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session)

from src.internal.authentications import (AuthenticationController, InvalidAccessError)
from src.internal.model_3d import Model3dController
from src.internal.users import UserController


def public_router(app: Flask):
    @app.get("/")
    @app.get("/home")
    def index():
        if "username" in session:
            username = session['username']
        users = UserController.pagination(0, 30)
        models3ds = Model3dController.pagination(0, 30)
        return render_template("layoute/index.html",
                               users = users,
                               model_3ds = models3ds)

    @app.route("/login", methods = ('GET', 'POST'))
    def login():
        if "username" in session:
            username = session['username']

        if request.method == 'POST':
            form_data = request.form

            username: str = form_data['username']
            password: str = form_data['password']

            try:
                account_response = AuthenticationController.login(username, password)
                session["username"] = account_response.username
                session["user_id"] = account_response.user_id


            except InvalidAccessError as err:
                message = "Username or password is invalid. Please try again"
                return render_template("layoute/login.html", error_message = message)
            else:
                return redirect("/home")
        return render_template("layoute/login.html")

    @app.route("/logout", methods = ['GET'])
    def logout():
        if "username" in session:
            session.pop('username', None)
            session.pop('user_id', None)

        return redirect('/login')
