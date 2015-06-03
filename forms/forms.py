from flask_wtf.form import Form
from wtforms.fields.simple import TextField, PasswordField, SubmitField
from wtforms import validators
from database.session import Get


class SignupForm(Form):
    email = TextField("Email", [validators.Required("Please enter your email.")
                                , validators.Email("Please enter your email")])

    nickname = TextField("Nickname")
    password = PasswordField('Password', [validators.Required('Please eneter \
        a password')])
    submit = SubmitField("Create account")

    # base class constructor
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        get = Get()
        user = get.user(email=self.email.data.lower())
        if user:
            self.email.errors.append("that email is already taken")
            return False
        else:
            return True
