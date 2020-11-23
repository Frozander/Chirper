"""
Chiper.Posts

This module handles the endpoints for post creation, editing, liking.
It also handles the same operations for comments (except editing).
"""

from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import current_user
from werkzeug.exceptions import abort

from chirper.auth import login_required
from chirper.database import db, Post, Comment
from chirper.forms import PostForm, CommentForm

bp = Blueprint('posts', __name__, url_prefix='/posts')


def get_one_post(id, check_author=True):
    """
    Params::

        id: (int) Id of the post to be returned

        check_author: (bool) Bypass author check. For moderator access.

    Returns::

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


@bp.route('/<b64:id>', methods=['GET', 'POST'])
@login_required
def post_page(id):
    """
    Endpoint: posts/<b64:id>

    Handles : GET, POST

    Post page. Contains posts like index but also shows and lets you send comments
    """

    post = Post.query.filter_by(id=id).first_or_404()
    comments = post.comments
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        new_comment = Comment(
            post_id=post.id,
            author_id=current_user.id,
            body=comment_form.body.data
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment has been added!', category='info')
        return redirect(url_for('posts.post_page', id=post.id))

    return render_template('posts/post.html', post=post, comments=comments, comment_form=comment_form)


@bp.route('/comment/<b64:id>/delete')
@login_required
def delete_comment(id):
    """
    Endpoint: comment/<b64:id>/delete

    Handles : GET, POST

    API endpoint for deleting comments. Needs authorization of the poster
    """

    comment = Comment.query.filter_by(id=id).first_or_404()

    if current_user.id == comment.author_id:
        db.session.delete(comment)
        db.session.commit()
    return redirect(request.referrer)


@bp.route('/comment/<b64:id>/<action>')
@login_required
def like_comment(id, action):
    """
    Endpoint: comment/<b64:id>/like

    Handles : GET, POST

    API endpoint for liking comments.
    """

    comment = Comment.query.filter_by(id=id).first_or_404()

    if action == 'like':
        current_user.like_comment(comment)
    elif action == 'unlike':
        current_user.unlike_comment(comment)

    db.session.commit()
    return redirect(request.referrer)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
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


@bp.route('/<b64:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Endpoint: posts/<b64:id>/edit

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
        next_page = request.args.get('next')

        return redirect(next_page or url_for('posts.post_page', id=post.id) or url_for('index'))
    else:
        post_form.title.data = post.title
        post_form.body.data = post.body
        return render_template('posts/edit.html', form=post_form, post=post)


@bp.route('/<b64:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    """
    Endpoint: posts/<b64:id>/delete

    Handles : POST

    API endpoint for deleting posts. Needs authorization of the poster
    """

    post = get_one_post(id)

    if current_user.id == post.author_id:
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted!', category='danger')
        return redirect(url_for('index'))
    flash('You cannot delete a post from someone else', category='danger')
    return redirect(url_for('index'))


@bp.route('/like/<b64:post_id>/<action>')
@login_required
def like_action(post_id, action):
    """
    Endpoint: /like/<b64:post_id>/<action>

    Handles : POST

    API endpoint for liking/unliking posts. Needs authorization of the poster
    """

    post = Post.query.filter_by(id=post_id).first_or_404()

    if action == 'like':
        current_user.like_post(post)
    elif action == 'unlike':
        current_user.unlike_post(post)

    db.session.commit()
    return redirect(request.referrer)
