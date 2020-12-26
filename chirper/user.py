"""
Chiper.USer

This module handles the endpoints for profile page and user utils.
"""

from os.path import join
import secrets
from PIL import Image
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user

from chirper.auth import login_required
from chirper.database import User, Post, db, PostLike
from chirper.forms import SettingsForm, UpdateForm
from chirper.obs import obscure

bp = Blueprint('user', __name__, url_prefix='/user')


def save_image(form_image, f_name):
    image_fn = f"{f_name}_{secrets.token_hex(4)}.png"
    image_path = join(current_app.root_path, 'static/img/profile', image_fn)

    output_size = (150, 150)
    i = Image.open(form_image).resize((300, 300))
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{error}", 'danger')


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
                    f_name = obscure.encode_base64(current_user.id)
                    img_file = save_image(image_new, f_name)
                    current_user.picture = img_file
                if password_new != "":
                    user.set_password(password_new)
                db.session.commit()
                flash("Valid settings have been updated!", category='info')
            else:
                flash_errors(update_form)
        else:
            flash("You must enter the old password to make changes",
                  category='warning')
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


@bp.route('/<b64:user_id>/follow', methods=['GET', 'POST'])
@login_required
def follow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('User not found!', 'danger')
        return redirect(url_for('index'))
    if user_id == current_user.id:
        flash('You can\'t follow yourself!', 'danger')
        return redirect(url_for('user.profile', user_id=user_id))
    u = current_user.follow(user)
    if u is None:
        flash(f'Cannot follow {user.username}!', user_id=user_id)
        return redirect(url_for('user.profile', user_id=user_id))
    db.session.add(u)
    db.session.commit()
    flash(f'You\'re now following {user.username}!', 'success')
    return redirect(url_for('user.profile', user_id=user_id))


@bp.route('/<b64:user_id>/unfollow', methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('User not found!', 'danger')
        return redirect(url_for('index'))
    if user_id == current_user.id:
        flash('You can\'t unfollow yourself!', 'danger')
        return redirect(url_for('user.profile', user_id=user_id))
    u = current_user.unfollow(user)
    if u is None:
        flash(f'Cannot unfollow {user.username}!', user_id=user_id)
        return redirect(url_for('user.profile', user_id=user_id))
    db.session.add(u)
    db.session.commit()
    flash(f'You have stopped following {user.username}!', 'success')
    return redirect(url_for('user.profile', user_id=user_id))
