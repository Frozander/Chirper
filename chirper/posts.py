from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import current_user
from werkzeug.exceptions import abort

from chirper.auth import login_required
from chirper.database import db, Post
from chirper.forms import PostForm

bp = Blueprint('posts', __name__, url_prefix='/posts')


def get_one_post(id, check_author=True):
    """
    get_one_post(id, check_author=True) -> Post, HTTPException
    Params:
        id: (int) Id of the post to be returned
        check_author: (bool) Bypass author check. For moderator access.
    Returns:
        Post: Post object with the data of the given post id
        HTTPException:
            404: Post does not exits
            403: Not authorized  
    """

    post = Post.query.get(int(id))

    if post is None:
        abort(404, f'Post id {id} does not exist.')

    if check_author and post.author_id != current_user.id:
        abort(403)

    return post


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    create() -> template
    Endpoint: posts/create
    Handles : GET, POST
    Post creation page.
    """

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
    """
    edit(id) -> template
    Endpoint: posts/<int:id>/edit
    Handles : GET, POST
    Post editing page, author can change the contents of the post or delete it
    """

    post = get_one_post(id)
    post_form = PostForm()

    if post_form.validate_on_submit():

        if post_form.delete.data:
            db.session.delete(post)
            db.session.commit()
            flash('Post has been deleted!', category='danger')
            return redirect(url_for('index'))

        post.title = post_form.title.data
        post.body = post_form.body.data

        db.session.commit()
        flash('Post has been updated!', category='info')
        return redirect(url_for('index'))
    else:
        post_form.title.data = post.title
        post_form.body.data = post.body
        return render_template('posts/edit.html', form=post_form, post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """
    delete(id) -> template
    Endpoint: posts/<int:id>/delete
    Handles : POST
    API endpoint for deleting posts. Needs authorization of the poster
    """

    post = get_one_post(id)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted!', category='danger')
        return redirect(url_for('index'))
