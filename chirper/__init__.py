"""
Chirper

Creates the app instance
"""

import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_required
from flask_nav import register_renderer
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

from . import auth, posts
from .database import db
from .navigation import CustomRenderer, nav

# Content Security Policy
# Allows using Cloudflare CDN to get Bootstrap
csp = {
    'default-src': [
        '\'self\'',
        'cdnjs.cloudflare.com'
    ]
}


def create_app(test_config=None):
    """
    create_app(test_config: mapping) -> App
    Params:
        test_config: (mapping) Used to configure the app.
    Returns:
        App: Created Flask App
    """

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
        os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_MIGRATE_REPO=os.path.join(
            app.instance_path, 'db_repository'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True
    )

    # Enable white-space trimming
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Laod the test config if passed in
        app.config.from_mapping(test_config)

    # For CSRF Protection
    csrf = CSRFProtect(app)
    # For Header Security
    talisman = Talisman(app, content_security_policy=csp)
    # Bootstrap Wrapper
    bootstrap = Bootstrap(app)
    # Initialize Database from database.py where models are created
    db.init_app(app)
    # Initialize flask-nav
    nav.init_app(app)
    register_renderer(app, 'custom', CustomRenderer)
    # Set-up login_manager
    auth.login_manager.init_app(app)
    auth.login_manager.login_view = 'auth/login'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)

    # TODO: Turn this to a infinite scroll using API calls with JSON returns
    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def index():
        post_list = posts.Post.query.all()

        return render_template('base.html', posts=post_list)

    app.add_url_rule('/index', '/')

    return app
