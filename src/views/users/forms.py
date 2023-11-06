from wtforms import Form, StringField, PasswordField, validators


class RegistrationUserForm(Form):
    full_name = StringField('Fullname', [validators.Length(min = 4, max = 25)])
    email = StringField('Email Address', [validators.Length(min = 6, max = 35)])
    pseudo = StringField('Pseudo', [validators.Length(min = 6, max = 35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
    ])
    confirm = PasswordField('Repeat Password')
