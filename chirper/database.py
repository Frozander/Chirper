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
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    picture = db.Column(db.String(20), unique=False,
                        nullable=False, server_default='default.png')

    posts = db.relationship(
        'Post', backref='user', lazy='dynamic', order_by='Post.created.desc()', cascade="all, delete-orphan")

    # Like System
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic'
    )

    # Comment System
    commented = db.relationship(
        'Comment',
        foreign_keys='Comment.author_id',
        backref='user', lazy='dynamic', order_by='Comment.created.desc()'
    )

    commentliked = db.relationship(
        'CommentLike',
        foreign_keys='CommentLike.user_id',
        backref='user', lazy='dynamic'
    )

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):  # If not liked
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):  # If liked
            CommentLike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id
            ).delete()

    def has_liked_comment(self, comment):
        return CommentLike.query.filter(
            CommentLike.user_id == self.id,
            CommentLike.comment_id == comment.id
        ).count() > 0

    def like_post(self, post):
        if not self.has_liked_post(post):  # If not liked
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):  # If liked
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id
            ).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id
        ).count() > 0

    def set_password(self, password: str):
        """
        Params::

            password: (string) Plaintext password to be hashed
        """

        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password: str):
        """
        Params::

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

    author_name = db.relationship('User', backref='post')

    # Like System
    likes = db.relationship('PostLike', backref='post',
                            lazy='dynamic', cascade="all, delete-orphan")

    # Comment System
    comments = db.relationship(
        'Comment', backref='post', lazy='dynamic', order_by='Comment.created.desc()', cascade="all, delete-orphan")


class PostLike(db.Model):
    """
    PostLike class to define Table structure on the database
    """

    __tablename__ = 'post_like'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Comment(db.Model):
    """
    Comment class to define Table structure on the database
    """

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.now())
    modified = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False, server_onupdate=db.func.now())
    body = db.Column(db.String, nullable=False)

    author_name = db.relationship('User', backref='comment')

    # Like System
    likes = db.relationship('CommentLike', backref='comment',
                            lazy='dynamic', cascade="all, delete-orphan")


class CommentLike(db.Model):
    """
    CommentLike class to define Table structure on the database
    """

    __tablename__ = 'comment_like'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
