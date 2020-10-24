"""
Chirper.Forms

Creates WTForms Classes for the various forms (LoginForm, RegisterForm etc.)
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """
    LoginForm class to be used in the /auth/login
    """

    email = StringField('E-Mail',
                        validators=[
                            DataRequired(),
                            Email("Enter a valid E-Mail")
                        ],
                        render_kw={'placeholder': 'Enter E-Mail'})
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(
                                     max=80, message="Max password length is 80 characters.")
                             ],
                             render_kw={'placeholder': 'Enter Password'})
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """
    RegisterForm class to be used in the /auth/register
    """

    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=3, max=20,
                                      message="Username has to be between 3-20 characters long.")
                           ],
                           render_kw={'placeholder': 'Enter Username'})
    email = StringField('E-Mail',
                        validators=[
                            DataRequired(),
                            Email("Enter a valid E-Mail")
                        ],
                        render_kw={'placeholder': 'Enter E-Mail'})
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(
                                     max=80, message="Max password length is 80 characters.")
                             ],
                             render_kw={'placeholder': 'Enter Password'})
    submit = SubmitField('Register')
