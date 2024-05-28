from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, length, Email
from models import Users


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email Address',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                           validators=[DataRequired()])
    submit = SubmitField('SIGN UP')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken please choose other username")
        
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken please choose other email")

class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('LOGIN')

class ForgotEmailForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('SUBMIT')

class NewPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('SUBMIT')
