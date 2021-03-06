from os import getenv, path

from dotenv import load_dotenv

load_dotenv()

# Read environment vars, if they don't exist use default
# You can set these Environment Variables by creating a .env file in the root of the repository
# Or add more variables depending on your choices. The ones that are displayed here should always exist
# Like SQLALCHEMY_DATABASE_URI, OBSCURE_SALT, SECRET_KEY etc. to provide a secure and consistent runtime
# With the intended actions like forcing SSL for Bootstrap CDN, Enabling CSRF Protection etc.

# Flask Values
FLASK_APP = getenv('FLASK_APP', 'chirper')
FLASK_ENV = getenv('FLASK_ENV', 'development')
# SERVER_NAME = getenv('SERVER_NAME', 'localhost')
SECRET_KEY = getenv('SECRET_KEY', 'dev')
DEBUG = getenv('DEBUG', False) in (True, 'True')

# Flask-Obscure salt
OBSCURE_SALT = int(getenv('OBSCURE_SALT', '0x77a592aa'), 16)

# SQLAlchemy Values
SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///' +
                                 path.abspath(path.join('./instance', 'app.db')))
# This should always be false
SQLALCHEMY_TRACK_MODIFICATIONS = bool(getenv(
    'SQLALCHEMY_TRACK_MODIFICATIONS', False))

# WTForms
WTF_CSRF_ENABLED = bool(getenv('WTF_CSRF_ENABLED', True))
# FLask Bootstrap
BOOTSTRAP_CDN_FORCE_SSL = bool(getenv('BOOTSTRAP_CDN_FORCE_SSL', True))

SESSION_COOKIE_SECURE = bool(getenv('SESSION_COOKIE_SECURE', True))

# Max Upload Size in MB
MAX_CONTENT_LENGTH = int(getenv('MAX_CONTENT_LENGTH', 2)) * 1024 * 1024
