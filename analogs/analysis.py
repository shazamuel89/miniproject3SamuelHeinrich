# Import Flask utilities for routing, flash messages, global user context, redirects, rendering, requests, and URL building
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

# Import abort to stop execution with HTTP errors
from werkzeug.exceptions import abort

# Import the login_required decorator to restrict certain routes
from analogs.auth import (login_required)

# Import the helper function to access the database
from analogs.db import get_db

# Create a blueprint named 'analysis' without a URL prefix
bp = Blueprint('analysis', __name__)

# Define a route for the index page of the analysis
@bp.route('/')
def index():
    # Connect to the database
    db = get_db()
    # Run a SQL query to fetch all analyses with their id, song_title, artist, body, created, author_id, and the user's username, sort by newest first
    analyses = db.execute(
        'SELECT a.id, a.song_title, a.artist, a.body, a.created, a.author_id, u.username'
        ' FROM analysis a JOIN user u ON a.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    # Render the index.html template passing in the analysis data
    return render_template('analysis/index.html', analyses=analyses)

@bp.route('/<int:id>')
def detail(id):
    db = get_db()

    # Fetch the analysis (no author check needed)
    analysis = get_analysis(id, check_author=False)

    # Fetch comments for this analysis
    comments = db.execute(
        '''
        SELECT c.body,
               c.created,
               u.username AS author
        FROM comment c
        LEFT JOIN user u ON c.author_id = u.id
        WHERE c.analysis_id = ?
        ORDER BY c.created ASC
        ''',
        (id,)
    ).fetchall()

    # Render the template with both analysis & comments
    return render_template('analysis/detail.html', analysis=analysis, comments=comments)

# Define a route for creating new analysis that accepts GET and POST
@bp.route('/create', methods=('GET', 'POST'))
# Wrap the route with the login_required decorator
@login_required
def create():
    # If the client submitted the form via POST
    if request.method == 'POST':
        # Extract the title and body from the form data
        song_title = request.form['song_title']
        artist = request.form['artist']
        body = request.form['body']
        error = None

        # Check that song title, artist, and body was provided
        if not song_title:
            error = 'Song title is required.'
        if not artist:
            error = 'Artist is required.'
        if not body:
            error = 'Body is required.'

        # If error occurred, flash it to the user
        if error is not None:
            flash(error)
        else:
            # Otherwise, insert the new analysis into the database
            db = get_db()
            db.execute(
                'INSERT INTO analysis (song_title, artist, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (song_title, artist, body, g.user['id'])
            )
            db.commit()
            # Redirect the user back to the index page
            return redirect(url_for('analysis.index'))

    # If GET or an error occurred, show the create form template
    return render_template('analysis/create.html')

# Helper function to fetch an analysis by id and optionally check ownership (will check ownership by default)
def get_analysis(id, check_author=True):
    # Run a SQL query to fetch the analysis and its data
    analysis = get_db().execute(
        'SELECT a.id, a.song_title, a.artist, a.body, a.created, a.author_id, u.username'
        ' FROM analysis a JOIN user u ON a.author_id = u.id'
        ' WHERE a.id = ?',
        (id,)
    ).fetchone()

    # If no analysis exists for this id, abort with 404
    if analysis is None:
        abort(404, f"Analysis id {id} doesn't exist.")

    # If we need to check author, and the logged-in user is not the owner, abort with 403
    if check_author and analysis['author_id'] != g.user['id']:
        abort(403)

    # Return the fetched analysis
    return analysis

# Define a route for updating an analysis given its id
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
# Update requires login
@login_required
def update(id):
    # Fetch the analysis by id and verify ownership
    analysis = get_analysis(id)

    # If the user submitted the update form via POST
    if request.method == 'POST':
        # Extract the new song_title, artist, and body from the form data
        song_title = request.form['song_title']
        artist = request.form['artist']
        body = request.form['body']
        error = None

        # Verify that song title, artist, and body was provided
        if not song_title:
            error = 'Song title is required.'
        if not artist:
            error = 'Artist is required.'
        if not body:
            error = 'Body is required.'

        # If error occurred, flash it to the user
        if error is not None:
            flash(error)
        else:
            # Otherwise, update the analysis in the database
            db = get_db()
            db.execute(
                'UPDATE analysis SET song_title = ?, artist = ?, body = ?'
                ' WHERE id = ?',
                (song_title, artist, body, id)
            )
            db.commit()
            # Redirect the user back to the index page
            return redirect(url_for('analysis.index'))

    # For GET or error, render the update template with the existing analysis data
    return render_template('analysis/update.html', analysis=analysis)

# Define a route to delete an analysis given its id, only accessed via POST
@bp.route('/<int:id>/delete', methods=('POST',))
# Delete requires login
@login_required
def delete(id):
    # Ensure the analysis exists and verify ownership
    get_analysis(id)
    # Delete the analysis from the database
    db = get_db()
    db.execute('DELETE FROM analysis WHERE id = ?', (id,))
    db.commit()
    # Redirect the user back to the index page
    return redirect(url_for('analysis.index'))