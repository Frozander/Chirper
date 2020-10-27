from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import current_user
from werkzeug.exceptions import abort

from chirper.auth import login_required
from chirper.database import db, Post
from chirper.forms import PostForm

bp = Blueprint('blog', __name__)


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
        return redirect(url_for('index'))

    return render_template('posts/create.html')
