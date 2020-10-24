from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
# import db for database management
from sqlalchemy import or_

from chirper.database import User, db
from chirper.forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.', category='danger')
    return redirect(url_for('auth.login'))

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
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_password(password=login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid E-Mail/Password Combination', category='danger')
        return redirect(url_for('auth.login'))
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
        existing_user = db.session.query(User).filter(
            or_(
                User.username==register_form.username.data,
                User.email==register_form.email.data)
            ).first()

        if existing_user is None:
            user = User(
                username=register_form.username.data,
                email=register_form.email.data
            )
            user.set_password(register_form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        flash('A user already exists with that E-Mail Address or Username!', category='danger')

    return render_template('auth/register.html',
                           title='Register',
                           form=register_form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
