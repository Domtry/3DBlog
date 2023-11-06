import uuid

from flask import session, render_template, redirect, request, Flask

from src.internal.model_3d import Model3dController
from src.internal.model_3d.schemas import Model3D as Model3DEntity
from src.internal.users import UserController
from src.views.model_3d.forms import RegistrationModel3DForm


def model_3d_router(app: Flask):
    @app.get("/model_3d/<string:model_3d_id>")
    def detail_model_3d(model_3d_id: str):
        if "username" in session:
            username = session['username']
        models_3d = Model3dController.get_model_3d(model_3d_id)
        return render_template("layoute/detail-page.html", detail_model = models_3d)

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
        form = RegistrationModel3DForm(request.form)
        if "username" not in session:
            return redirect('/login')

        user_id = session["user_id"]
        user = UserController.get_user(user_id)

        if request.method == 'POST':
            model_3d = Model3DEntity(
                id = str(uuid.uuid4()),
                label = form.label.data,
                image_path = form.image_path.data,
                description = form.describe.data,
                user = user
            )

            Model3dController.create_model_3d(model_3d)
            return redirect('/store')

        return render_template("layoute/create_model_3d.html", user = user)
