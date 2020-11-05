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

    __tablename__ = 'user'

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


class Post(db.Model):
    """
    Post class to define Table structure on the database
    """

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.now())
    modified = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False, server_onupdate=db.func.now())
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)


class PostLike(db.Model):
    """
    PostLike class to define Table structure on the database
    """

    __tablename__ = 'post_like'

    id = db.Column(db.Integer, primary_key=True)
    liked_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    liker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
