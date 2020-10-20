import os

SECRET_KEY='dev'
SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'app.db')
SQLALCHEMY_MIGRATE_REPO=os.path.join(app.instance_path, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS=False