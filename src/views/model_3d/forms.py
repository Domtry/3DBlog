from wtforms import Form, TextAreaField, URLField, validators, StringField


class RegistrationModel3DForm(Form):
    label = StringField('Labal', [validators.Length(min = 4, max = 25)])
    image_path = URLField('Image Path', [validators.Length(min = 6, max = 35)])
    describe = TextAreaField('Description', [validators.Length(min = 6, max = 35)])
