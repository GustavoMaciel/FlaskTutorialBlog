from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.users.models import User

common_validators = [DataRequired()]
username_validators = common_validators + [Length(min=5, max=20)]
email_validators = common_validators + [Email()]
confirm_password_validators = common_validators + [EqualTo('password')]


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=username_validators)
    email = StringField("Email", validators=email_validators)
    password = PasswordField("Password", validators=common_validators)
    confirm_password = PasswordField("Confirm Password", validators=confirm_password_validators)

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already taken')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=email_validators)
    password = PasswordField("Password", validators=common_validators)
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):

    username = StringField("Username", validators=username_validators)
    email = StringField("Email", validators=email_validators)
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user and user != current_user:
                raise ValidationError('The email is already taken')


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=email_validators)
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=common_validators)
    confirm_password = PasswordField("Confirm Password", validators=confirm_password_validators)

    submit = SubmitField("Reset Password")

