import pytest
from src import DatabaseManager


def test_dbpath():
    db_path = DatabaseManager.get_db_path()
    assert db_path.exists() is True
