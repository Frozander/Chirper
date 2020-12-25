"""
Chiper.USer

This module handles the endpoints for profile page and user utils.
"""

from os.path import join, splitext
import secrets
from PIL import Image
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user

from chirper.auth import login_required
from chirper.database import User, Post, db, PostLike
from chirper.forms import SettingsForm, UpdateForm

bp = Blueprint('user', __name__, url_prefix='/user')


def save_image(form_image):
    r_name = secrets.token_hex(8)
    _, ext = splitext(form_image.filename)
    image_fn = r_name + ext
    image_path = join(current_app.root_path, 'static/img/profile', image_fn)

    output_size = (300, 300)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn


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
    settings_form = SettingsForm()
    update_form = UpdateForm()
    settings_form.username.render_kw = {'placeholder': user.username}
    settings_form.email.render_kw = {'placeholder': user.email}

    if settings_form.is_submitted():
        username_new = settings_form.username.data
        email_new = settings_form.email.data
        password_new = settings_form.password_new.data
        password_old = settings_form.password_old.data
        image_new = settings_form.picture.data

        update_form.email.data = email_new or user.email
        update_form.username.data = username_new or user.username

        if user.check_password(password_old):
            if update_form.validate():
                user.username = update_form.username.data
                user.email = update_form.email.data
                if image_new:
                    img_file = save_image(image_new)
                    current_user.picture = img_file
                if password_new != "":
                    user.set_password(password_new)
                db.session.commit()
                flash("Valid settings have been updated!", category='info')
        else:
            flash("You must enter the old password to make changes",
                  category='danger')
    img = url_for('static',
                  filename='img/profile' + current_user.picture)
    return render_template('user/settings.html', user=user, form=settings_form)


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


@bp.route('/<b64:user_id>/comments', methods=['GET', 'POST'])
@login_required
def comments(user_id):
    """
    Endpoint: /<b64:user_id>/comments

    Handles : POST, GET

    API endpoint for rendering the profile page.
    And the content part of the page that contains the comments of the user.
    """

    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user/comments.html', user=user, comments=user.commented)
