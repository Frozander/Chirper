import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

from . import auth
from .database import db


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object('config', silent=True)
    else:
        # Laod the test config if passed in
        app.config.from_mapping(test_config)
    
    # For CSRF Protection
    csrf = CSRFProtect(app)
    # Bootstrap Wrapper
    bootstrap = Bootstrap(app)
    # Initialize Database from database.py where models are created
    db.init_app(app)
    # Register Blueprints
    auth.login_manager.init_app(app)
    auth.login_manager.login_view = 'auth/login'
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.register_blueprint(auth.bp)
    
    # TEMP
    @app.route('/')
    def index():
        return render_template('base.html')
    
    return app