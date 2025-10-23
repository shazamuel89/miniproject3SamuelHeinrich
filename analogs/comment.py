from flask import Blueprint, request, redirect, url_for, g, flash
from analogs.db import get_db

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create', methods=('POST',))
def create():
    # Hidden input in the form for analysis_id expected
    analysis_id = request.form['analysis_id']
    body = request.form['body']
    if not body.strip():
        flash("Comment cannot be empty.")
        return redirect(url_for('analysis.detail', id=analysis_id))

    db = get_db()

    # If user is logged in, associate user with comment, otherwise Anonymous
    user_id = g.user['id'] if hasattr(g, 'user') and g.user else None

    db.execute(
        'INSERT INTO comment (analysis_id, user_id, body)'
        ' VALUES (?, ?, ?)',
        (analysis_id, user_id, body)
    )
    db.commit()

    return redirect(url_for('analysis.detail', id=analysis_id))

@bp.route('/list/<int:analysis_id>', methods=('GET',))
def list_for_analysis(analysis_id):
    # Fetch all comments for the analysis

    db = get_db()
    comments = db.execute(
        'SELECT c.id, c.body, c.created, u.username'
        ' FROM comment c LEFT JOIN user u ON c.author_id = u.id'
        ' WHERE c.analysis_id = ?'
        ' ORDER BY c.created DESC',
        (analysis_id,)
    ).fetchall()

    return comments