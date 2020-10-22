from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()], 
                        render_kw={'placeholder': 'Enter E-Mail'})
    password = PasswordField('password', validators=[DataRequired(), Length(max=80, message="Max password length is 80 characters.")],
                             render_kw={'placeholder': 'Enter Password'})
    remember_me = BooleanField('remember_me', default=False)

# TODO: ADD REGISTER FORM
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()], 
                        render_kw={'placeholder': 'Enter E-Mail'})
    password = PasswordField('password', validators=[DataRequired(), Length(max=80, message="Max password length is 80 characters.")],
                             render_kw={'placeholder': 'Enter Password'})
    remember_me = BooleanField('remember_me', default=False)