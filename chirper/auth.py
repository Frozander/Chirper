from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
# import db for database management

login_manager = LoginManager()
from chirper.database import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/', methods=['GET', 'POST'])
def auth():
    return "<h1>Authentication Page</h1>"
    
    