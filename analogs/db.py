
# Allows interaction with SQLite databases
import sqlite3
# Allows interpreting timestamps when converting values
from datetime import datetime

# Creates CLI commands for Flask
import click
# Import current_app to access the app config, and g to store database connection during a request
from flask import current_app, g

# Define a function to retrieve or create the database connection
def get_db():
    # If there is no db connection stored in g, create one
    if 'db' not in g:
        # Connect to the database path defined in the app config
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Configure the database to return rows as dictionaries
        g.db.row_factory = sqlite3.Row

    # Return the existing or newly created db connection
    return g.db

# Define a function to close the db connection after a request ends
def close_db(e=None):
    # Remove and retrieve the stored db connection from g if it exists
    db = g.pop('db', None)

    # If a db connection was present, close it
    if db is not None:
        db.close()

# Define a function to initialize the db using schema.sql
def init_db():
    # Get the db connection
    db = get_db()

    # Open the schema.sql file from the application resources
    with current_app.open_resource('schema.sql') as f:
        # Execute the entire SQL script to create/reset tables
        db.executescript(f.read().decode('utf8'))

# Define a click command runnable from the CLI called 'init-db'
@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables
    init_db()
    # Output confirmation to the CLI that initialization occurred
    click.echo('Initialized the database.')

# Define a function to register db-related handlers to the Flask app
def init_app(app):
    # Register the close_db function to run after each request ends
    app.teardown_appcontext(close_db)
    # Add the init_db_command into the Flask CLI commands
    app.cli.add_command(init_db_command)

# Register a custom SQLite converter for "timestamp" columns to convert ISO strings to datetime objects
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)