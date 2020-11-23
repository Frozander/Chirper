from os import getenv, path

from dotenv import load_dotenv

env_path = path.abspath('../.env')
load_dotenv(env_path)

# Read environment vars, if they don't exist use default
FLASK_APP = getenv('FLASK_APP', 'chirper')
FLASK_ENV = getenv('FLASK_ENV', 'development')
SECRET_KEY = getenv('SECRET_KEY', 'dev')
DEBUG = getenv('DEBUG', False) in (True, 'True')
OBSCURE_SALT = int(getenv('OBSCURE_SALT', '0x77a592aa'), 16)
