from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired()], 
                        render_kw={'placeholder': 'Enter E-Mail'})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=80, message="Max password length is 80 characters.")],
                             render_kw={'placeholder': 'Enter Password'})
    remember_me = BooleanField('Remember Me', default=False)

class RegisterForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()], 
                        render_kw={'placeholder': 'Enter E-Mail'})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=80, message="Max password length is 80 characters.")],
                             render_kw={'placeholder': 'Enter Password'})