from flask import current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
        
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(15), unique=True, nullable=False)
        email = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(80), unique=False, nullable=False)
        
        def set_password(self, password):
                self.password = generate_password_hash(password, method='sha256')
        
        def check_password(self, password):
                return check_password_hash(self.password, password)

        def __repr__(self):
                return f'<User {self.username}>'
               