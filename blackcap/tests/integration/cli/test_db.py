"""CLI db commands tests."""
# flake8: noqa

from click.testing import CliRunner

from blackcap.cli.db import db

runner = CliRunner()


def test_db_reset() -> None:
    res = runner.invoke(db)
    assert res.exit_code == 0
