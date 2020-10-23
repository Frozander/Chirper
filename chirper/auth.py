from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
# import db for database management

login_manager = LoginManager()
from chirper.database import User
from chirper.forms import LoginForm, RegisterForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_request
def before_request():
    g.user = current_user

@bp.route('/login', methods=['POST', 'GET'])
def login():
    # Skip if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        return redirect(url_for('index'))
    
    return render_template('auth/login.html',
                           title='Sign In',
                           form=login_form)

# TODO: ADD REGISTER ENDPOINT
@bp.route('/register', methods=['POST', 'GET'])
def register():
    # Skip if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html',
                           title='Register',
                           form=register_form)