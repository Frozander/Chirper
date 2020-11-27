from os import getenv, path

from dotenv import load_dotenv

env_path = path.abspath('../.env')
load_dotenv(env_path)

# Read environment vars, if they don't exist use default

# Flask Values
FLASK_APP = getenv('FLASK_APP', 'chirper')
FLASK_ENV = getenv('FLASK_ENV', 'development')
SECRET_KEY = getenv('SECRET_KEY', 'dev')
DEBUG = getenv('DEBUG', False) in (True, 'True')

# Flask-Obscure salt
OBSCURE_SALT = int(getenv('OBSCURE_SALT', '0x77a592aa'), 16)

# SQLAlchemy Values
SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///' +
                                 path.abspath(path.join('./instance', 'app.db')))
# This should always be false
SQLALCHEMY_TRACK_MODIFICATIONS = getenv(
    'SQLALCHEMY_TRACK_MODIFICATIONS', False)

# WTForms
WTF_CSRF_ENABLED = getenv('WTF_CSRF_ENABLED', True)
# FLask Bootstrap
BOOTSTRAP_CDN_FORCE_SSL = getenv('BOOTSTRAP_CDN_FORCE_SSL', True)
