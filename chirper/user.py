from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import current_user
from werkzeug.exceptions import abort

from chirper.auth import login_required
from chirper.database import db, Post, Comment, User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    user_posts = Post.query.filter_by(
        author_id=user_id).order_by(Post.created.desc()).all()

    return render_template('user/profile.html', user=user, posts=user_posts)
