from dotenv import load_dotenv
from os import getenv, path

env_path = path.abspath('../.env')
load_dotenv(env_path)

# Read environment vars, if they don't exist use default
FLASK_APP = getenv('FLASK_APP', 'chirper')
FLASK_ENV = getenv('FLASK_ENV', 'development')
SECRET_KEY = getenv('SECRET_KEY', 'dev')
DEBUG = getenv('DEBUG', False) in (True, 'True')
