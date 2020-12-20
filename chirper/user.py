"""
Chiper.USer

This module handles the endpoints for profile page and user utils.
"""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from chirper.auth import login_required
from chirper.database import User, Post, db, PostLike
from chirper.forms import UploadProfileForm

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<b64:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    """
    Endpoint: /<b64:user_id>

    Handles : POST, GET

    API endpoint for rendering the profile page.
    And the content part of the page that contains the posts of the user.
    """

    user = User.query.filter_by(id=user_id).first_or_404()
    posts = user.posts
    return render_template('user/profile.html', user=user, posts=posts)


@bp.route('/<b64:user_id>/settings', methods=['GET', 'POST'])
@login_required
def settings(user_id):
    """
    Endpoint: /<b64:user_id>/settings

    Handles : POST, GET

    API endpoint for rendering the profile page.
    And the content part of the page that contains the ProfileSettings form.
    """

    user = User.query.filter_by(id=user_id).first_or_404()
    if current_user.id != user.id:
        flash('You cannot see others settings', category='danger')
        return redirect(url_for('user.profile', user_id=user_id))
    upload_form = UploadProfileForm()
    return render_template('user/settings.html', user=user, upload_form=upload_form)


@bp.route('/<b64:user_id>/liked', methods=['GET', 'POST'])
@login_required
def liked(user_id):
    """
    Endpoint: /<b64:user_id>/liked

    Handles : POST, GET

    API endpoint for rendering the profile page.
    And the content part of the page that contains the posts that user liked.
    """

    user = User.query.filter_by(id=user_id).first_or_404()
    posts = db.session.query(Post).join(
        PostLike, Post.id == PostLike.post_id).filter(PostLike.user_id == user_id).order_by(Post.created.desc())
    return render_template('user/liked.html', user=user, posts=posts)


@ bp.route('/<b64:user_id>/comments', methods=['GET', 'POST'])
@ login_required
def comments(user_id):
    """
    Endpoint: /<b64:user_id>/comments

    Handles : POST, GET

    API endpoint for rendering the profile page.
    And the content part of the page that contains the comments of the user.
    """

    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user/comments.html', user=user, comments=user.commented)
