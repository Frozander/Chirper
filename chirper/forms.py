"""
Chirper.Forms

Creates WTForms Classes for the various forms (LoginForm, RegisterForm etc.)
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField)
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


class PostForm(FlaskForm):
    """
    RegisterForm class to be used in the /posts/create and /posts/edit
    """

    title = StringField('Title',
                        validators=[
                            DataRequired(),
                            Length(min=3, max=80,
                                   message="Title must have 3-50 characters")
                        ],
                        render_kw={'placeholder': 'Enter Title'})
    body = TextAreaField('Message',
                         validators=[
                             DataRequired(),
                             Length(min=3, max=512,
                                    message="Content must have 3-240 characters")
                         ],
                         render_kw={'placeholder': 'Share your thoughts...'})
    submit = SubmitField('Post')
    delete = SubmitField('Delete')


class CommentForm(FlaskForm):
    """
    CommentForm class to be used in the comment section in the /posts/<b64:id>
    """

    body = TextAreaField('Message',
                         validators=[
                             DataRequired(),
                             Length(min=3, max=256,
                                    message="Content must have 3-240 characters")
                         ],
                         render_kw={'placeholder': 'Share your thoughts...'})
    submit = SubmitField('Post')


class UploadProfileForm(FlaskForm):
    """
    UploadProfileForm class
    """

    upload = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Upload')


class SettingsForm(FlaskForm):
    """
    SettingsForm class
    """
    username = StringField('Username',
                           validators=[
                               Length(min=3, max=20,
                                      message="Username has to be between 3-20 characters long.")
                           ],
                           render_kw={'placeholder': 'Username'})
    email = StringField('E-Mail',
                        validators=[
                            Email("Enter a valid E-Mail")
                        ],
                        render_kw={'placeholder': 'E-Mail'})
    password_new = PasswordField('New Password',
                                 validators=[
                                     Length(
                                         max=80, message="Max password length is 80 characters.")
                                 ],
                                 render_kw={'placeholder': 'New Password'})
    password_old = PasswordField('Old Password',
                                 validators=[
                                     Length(
                                         max=80, message="Max password length is 80 characters.")
                                 ],
                                 render_kw={'placeholder': 'Old Password'})

    submit = SubmitField('Save')


class UpdateForm(FlaskForm):
    """
    UpdateForm class
    """

    username = StringField('Username',
                           validators=[
                               Length(min=3, max=20,
                                      message="Username has to be between 3-20 characters long.")
                           ],
                           render_kw={'placeholder': 'Username'})
    email = StringField('E-Mail',
                        validators=[
                            Email("Enter a valid E-Mail")
                        ],
                        render_kw={'placeholder': 'E-Mail'})
