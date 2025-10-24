# INF601 - Advanced Programming in Python
# Samuel Heinrich
# Mini Project 3

# functools helps wrap view functions without losing their metadata
import functools

# Import flask utilities for routing, flashing messages, sessions, rendering, etc.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# Import utilities to hash passwords and verify them securely
from werkzeug.security import check_password_hash, generate_password_hash

# Import the get_db function to interact with the database
from analogs.db import get_db

# Create a blueprint named 'auth' with URL prefix '/auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register a route for /register that allows GET and POST requests
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # If the request method is POST, the user is submitting the register form
    if request.method =='POST':
        # Retrieve the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        # Connect to the database
        db = get_db()

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # No error yet, so try to insert the user's data into the database
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            # Catch error for a duplicate username
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # If the insert succeeded, redirect to the login page
                return redirect(url_for("auth.login"))

        # Flash any potential error to the user
        flash(error)

    # Render the register template for GET (after checking for POST) or after errors
    return render_template('auth/register.html')

# Register a route for /login that allows GET and POST requests
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # If the request method is POST, the user is submitting the login form
    if request.method == 'POST':
        # Retrieve the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        # Connect to the database
        db = get_db()
        error = None
        # Select the first row matching the username from the user table
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # If no such user exists, or the password is incorrect, set an error
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # If there was no error, log the user in by storing user_id in session
        if error is None:
            # Clear any existing session data
            session.clear()
            # Store the user_id in the session
            session['user_id'] = user['id']
            # Redirect to the index page
            return redirect(url_for('index'))

        # Flash any potential error to the user
        flash(error)

    # Render the login template for GET (after checking for POST) or after errors
    return render_template('auth/login.html')

# Run before every request to determine if a user is currently logged in
@bp.before_app_request
def load_logged_in_user():
    # Retrieve the stored user_id from the session
    user_id = session.get('user_id')

    # If there is no user_id in session, set g.user to None
    if user_id is None:
        g.user = None
    # Otherwise, fetch the user data and store it in g.user
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# Register a route for /logout that logs the user out
@bp.route('/logout')
def logout():
    # Clear all session data to log the user out
    session.clear()
    # Redirect to the index page after logout
    return redirect(url_for('index'))

# Define a decorator that forces a user to be logged in before accessing a view
def login_required(view):
    # Use functools.wraps so the wrapped view keeps its original name and metadata
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # If g.user is None, the user is not logged in, so redirect to the login page
        if g.user is None:
            return redirect(url_for('auth.login'))

        # Otherwise, return the view function with the original arguments
        return view(**kwargs)

    # Return the wrapped view for use as a decorator
    return wrapped_view