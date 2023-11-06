import uuid

from flask import Flask, render_template, request, redirect

from .forms import RegistrationUserForm

from src.internal.users import UserController
from src.internal.users.schemas import Users as UserEntity

from src.internal.accounts import AccountController
from src.internal.accounts import AccountEntity


def user_router(app: Flask):
    @app.route("/inscription", methods = ('GET', 'POST'))
    def inscription():
        form = RegistrationUserForm(request.form)
        if request.method == 'POST':
            user = UserEntity(
                id = str(uuid.uuid4()),
                name = form.full_name.data,
                email = form.email.data,
                pseudo = form.pseudo.data
            )

            user_response = UserController.create_user(user)

            account = AccountEntity(
                username = user_response.email,
                password = form.password.data,
                user = user_response
            )

            AccountController.create_account(account)
            return redirect('/login')
        return render_template("layoute/inscription.html")
