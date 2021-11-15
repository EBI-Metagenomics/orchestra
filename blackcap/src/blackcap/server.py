"""Server factory."""

from typing import Callable

from blackcap.configs.base import BaseConfig
from blackcap.routes.job import job_bp
from blackcap.routes.schedule import schedule_bp
from blackcap.routes.status import status_bp
from blackcap.routes.user import user_bp
from blackcap.tasks import init_celery
from blackcap.workers import celery_app

from flask import Flask

from logzero import logger


def register_extensions(app: Flask) -> None:
    """Register extension.

    Args:
        app (Flask): Flask app
    """
    init_celery(app, celery_app)
    logger.info("Registered extensions")


def register_blueprints(app: Flask) -> None:
    """Register blueprints.

    Args:
        app (Flask): Flask app
    """
    app.register_blueprint(status_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(schedule_bp)
    logger.info("Registered blueprints")


def create_app(
    config: BaseConfig,
    register_ext: Callable[[Flask], None] = register_extensions,
    register_bp: Callable[[Flask], None] = register_blueprints,
) -> Flask:
    """Create a Flask App.

    Args:
        config (BaseConfig): App config
        register_ext (Callable[[Flask], None]): Function to register extensions
        register_bp (Callable[[Flask], None]): Function to register Blueprints

    Returns:
        Flask: Flask app
    """
    logger.info("Creating a flask app...")
    app = Flask(config.FLASK_APP)
    logger.info(f"Flask app created: {app.import_name}")

    # Load config
    app.config.from_object(config)
    logger.info(f"Config loaded: {type(config).__name__}")

    # Register extension
    register_ext(app)

    # Register blueprints
    register_bp(app)

    return app
