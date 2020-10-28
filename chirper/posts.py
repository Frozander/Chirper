from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import current_user
from werkzeug.exceptions import abort

from chirper.auth import login_required
from chirper.database import db, Post
from chirper.forms import PostForm, DeleteForm

bp = Blueprint('posts', __name__, url_prefix='/posts')


def get_one_post(id, check_author=True):
    post = Post.query.get(int(id))

    if post is None:
        abort(404, f'Post id {id} does not exist.')

    if check_author and post.author_id != current_user.id:
        abort(403)

    return post


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    if not current_user.is_authenticated:
        flash('You are not logged in!', category='danger')
        return redirect(url_for('auth.login'))

    post_form = PostForm()

    if post_form.validate_on_submit():
        new_post = Post(author_id=current_user.id,
                        title=post_form.title.data,
                        body=post_form.body.data
                        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post has been created!', category='info')
        return redirect(url_for('index'))

    return render_template('posts/create.html',
                           form=post_form)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = get_one_post(id)
    post_form = PostForm()
    delete_form = DeleteForm()

    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.body = post_form.body.data

        db.session.commit()
        flash('Post has been updated!', category='info')
        return redirect(url_for('index'))
    else:
        post_form.title.data = post.title
        post_form.body.data = post.body
        return render_template('posts/edit.html', form=post_form, del_form=delete_form, post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        post = get_one_post(id)
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted!', category='danger')
        return redirect(url_for('index'))
