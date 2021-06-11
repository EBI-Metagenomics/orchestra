"""Server factory."""

from conductor.configs.base import BaseConfig
from conductor.extensions import celery_app, init_celery
from conductor.routes.job import job_bp

from flask import Flask

from logzero import logger


def create_app(config: BaseConfig) -> Flask:
    """Create a Flask App.

    Args:
        config (BaseConfig): App config

    Returns:
        Flask: Flask app
    """
    logger.info("Creating a flask app...")
    app = Flask(__name__)
    logger.info(f"Flask app created: {app.import_name}")

    # Load config
    app.config.from_object(config)
    logger.info(f"Config loaded: {type(config).__name__}")

    # Register extension
    register_extensions(app)

    # Register blueprints
    register_blueprints(app)

    return app


def register_extensions(app: Flask) -> None:
    """Register extension.

    Args:
        app (Flask): Flask app
    """
    init_celery(app, celery_app)


def register_blueprints(app: Flask) -> None:
    """Register blueprints.

    Args:
        app (Flask): Flask app
    """
    app.register_blueprint(job_bp)
