from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session)

from src.internal.accounts import AccountController
from src.internal.accounts import AccountEntity
from src.internal.authentications import (AuthenticationController, InvalidAccessError)
from src.internal.model_3d import Model3dController
from src.internal.model_3d.schemas import Model3D as Model3DEntity
from src.internal.users import UserController
from src.internal.users.schemas import Users as UserEntity


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

    @app.get("/model_3d/<string:model_3d_id>")
    def detail_model_3d(model_3d_id: str):
        if "username" in session:
            username = session['username']
        models_3d = Model3dController.get_model_3d(model_3d_id)
        return render_template("layoute/detail-page.html", detail_model = models_3d)

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

    @app.route("/inscription", methods = ('GET', 'POST'))
    def inscription():
        if request.method == 'POST':
            form_data = request.form
            user = UserEntity(
                name = form_data['full_name'],
                email = form_data['email'],
                pseudo = form_data['pseudo']
            )

            user_response = UserController.create_user(user)

            account = AccountEntity(
                username = user_response.email,
                password = form_data['password'],
                user = user_response
            )

            AccountController.create_account(account)
            return redirect('/login')
        return render_template("layoute/inscription.html")

    @app.route("/store", methods = ['GET'])
    def store():
        if "username" in session:
            user_id = session["user_id"]

            user = UserController.get_user(user_id)
            model_3ds = Model3dController.get_model_3d_user_id(user_id)

            return render_template(
                "layoute/store.html", user = user, contents = model_3ds)
        else:
            return redirect('/login')

    @app.route("/store/new_model_3d", methods = ['GET', 'POST'])
    def create_model_3d():
        if "username" not in session:
            return redirect('/login')

        user_id = session["user_id"]
        user = UserController.get_user(user_id)

        if request.method == 'POST':
            form_data = request.form
            model_3d = Model3DEntity(
                label = form_data['label'],
                image_path = form_data['image_path'],
                description = form_data['describe'],
                user = user
            )

            Model3dController.create_model_3d(model_3d)
            return redirect('/store')

        return render_template("layoute/create_model_3d.html", user = user)

    @app.route("/logout", methods = ['GET'])
    def logout():
        if "username" in session:
            session.pop('username', None)
            session.pop('user_id', None)

        return redirect('/login')
