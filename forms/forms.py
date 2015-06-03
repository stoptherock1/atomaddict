from flask_wtf.form import Form
from wtforms.fields.simple import TextField, PasswordField, SubmitField
from wtforms import validators
from database.session import Get


class SignupForm(Form):
    email_sign_up = TextField("Email", [validators.Required("Please enter \
        your email."), validators.Email("Please enter your email")])

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
        user = get.user(email=self.email_sign_up.data.lower())
        get.close_session()
        if user:
            self.email_sign_up.errors.append("that email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email_sign_in = TextField("Email",
                              [validators.Required("Please enter your \
                              email address"),
                               validators.Email("Please enter your email \
                               address")])
    password = PasswordField('Password',
                             [validators.Required("Please enter a password")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        get = Get()
        user = get.user(email=self.email_sign_in.data.lower())
        get.close_session()
        if user and user.password == self.password.data:
            return True
        else:
            self.email_sign_in.errors.append("Invalid email or password")
            return False
