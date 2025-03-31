import pytest
from src import KeyboardManager


def test_hotkeyconfig():
    kb = KeyboardManager()
    assert kb._hotkey_config is not None
