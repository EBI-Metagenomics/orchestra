"""WSGI module."""

from conductor import global_config
from conductor.server import create_app

app = create_app(global_config)

if __name__ == "__main__":
    app.run()
