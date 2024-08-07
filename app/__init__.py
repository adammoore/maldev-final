"""
Initialize the Flask application and its extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_name: The name of the configuration to use (default: 'default')

    Returns:
        A configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app import routes
    app.register_blueprint(routes.main)

    return app

# Make sure create_app is available when importing from app
__all__ = ['create_app', 'db']