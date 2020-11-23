from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import current_user
from werkzeug.exceptions import abort

from chirper.auth import login_required
from chirper.database import db, Post, Comment, User
from chirper.forms import UploadProfileForm

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<b64:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    posts = user.posts
    return render_template('user/profile.html', user=user, posts=posts)


@bp.route('/<b64:user_id>/settings', methods=['GET', 'POST'])
@login_required
def settings(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    upload_form = UploadProfileForm()
    return render_template('user/settings.html', user=user, upload_form=upload_form)


@bp.route('/<b64:user_id>/liked', methods=['GET', 'POST'])
@login_required
def liked(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user/liked.html', user=user)


@bp.route('/<b64:user_id>/comments', methods=['GET', 'POST'])
@login_required
def comments(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user/comments.html', user=user)
