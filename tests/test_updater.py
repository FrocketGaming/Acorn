import pytest
from src import UpdateManager


def test_latest_version():
    latest = UpdateManager.get_latest_version()
    assert latest is None
