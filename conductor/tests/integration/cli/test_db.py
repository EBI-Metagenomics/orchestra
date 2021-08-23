"""CLI db commands tests."""
# flake8: noqa

from click.testing import CliRunner

from conductor.cli.db import reset

runner = CliRunner()


def test_db_reset() -> None:
    res = runner.invoke(reset)
    assert res.exit_code == 0
