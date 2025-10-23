import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'analogs.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import the database module and initialize the database with the app
    from . import db
    db.init_app(app)

    # Import the auth blueprint and register it with the app
    from . import auth
    app.register_blueprint(auth.bp)

    # Import the analysis blueprint and register it with the app
    from . import analysis
    app.register_blueprint(analysis.bp)
    # Add the root URL rule to map to the analysis index endpoint
    app.add_url_rule('/', endpoint='index')

    # Return the fully configured application instance
    return app