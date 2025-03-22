import pytest
from src import DatabaseManager, SnippetManager
import polars as pl


def test_load_snippets():
    sm = SnippetManager()
    results = sm.load_snippets()
    assert results


def test_get_snippets():
    sm = SnippetManager()
    results = sm.get_snippets()
    assert len(results) > 0
