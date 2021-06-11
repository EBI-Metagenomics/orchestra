"""WSGI module."""

from conductor.configs import Config, get_config
from conductor.server import create_app

default_config = get_config(Config.DEFAULT)
app = create_app(default_config)
