"""
This module initializes the Flask application and its extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_class: The configuration class to use (default: Config)

    Returns:
        A configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import routes
    app.register_blueprint(routes.main)

    return app
