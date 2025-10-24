# INF601 - Advanced Programming in Python
# Samuel Heinrich
# Mini Project 3

import os

from flask import (Blueprint, render_template, request, redirect, url_for, flash, current_app, g)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db
from .auth import login_required

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def profile():
    db = get_db()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        file = request.files.get('profile_picture')

        error = None

        # Validate username
        if not username:
            error = "Username is required."

        # Handle username update
        if error is None and username != g.user['username']:
            db.execute(
                'UPDATE user SET username=? WHERE id=?',
                (username, g.user['id'])
            )
            db.commit()

        # Handle password update (only if provided)
        if password:
            hashed = generate_password_hash(password)
            db.execute(
                'UPDATE user SET password=? WHERE id=?',
                (hashed, g.user['id'])
            )
            db.commit()

        # Handle image upload if provided
        if file and file.filename != '':
            if not allowed_file(file.filename):
                error = "File type not allowed. Please upload a PNG, JPG, JPEG, or GIF."
            else:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename
                )
                file.save(upload_path)

                # store filename in database
                db.execute(
                    'UPDATE user SET profile_picture=? WHERE id=?',
                    (filename, g.user['id'])
                )
                db.commit()

        if error:
            flash(error)
        else:
            flash("Profile updated.")
            return redirect(url_for('profile.profile'))

    return render_template('profile/profile.html', user=g.user)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS