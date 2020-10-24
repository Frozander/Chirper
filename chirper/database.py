"""
Chirper.Database

Creates the database instance and the models
"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User class to define Table structure on the database
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    def set_password(self, password):
        """
        set_password(self, password: string)
        Params:
            password: (string) Plaintext password to be hashed
        """
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """
        check_password(self, password: string)
        Params:
            password: (string) Plaintext password to be hashed
             and checked againt the stored password hash
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
