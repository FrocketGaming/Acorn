from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
from pathlib import Path
import json
from src.data.database_manager import DatabaseManager


class KeyboardManager(QObject):
    hotkey_activated = pyqtSignal()  # Signal emitted when hotkey is activated
    show_hide_window = pyqtSignal()  # Signal to toggle window visibility
    enter_key_pressed = pyqtSignal()  # Signal for the Enter key press

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._hotkey_config = self.db.read_database("hotkeys", "hotkey")["hotkey"][0]
        self.is_active = False  # Track whether the window is active
        self.setup_hotkey_listener()
        self.setup_enter_listener()

    @property
    def hotkey_config(self) -> str:
        """Getter for the hotkey configuration."""

        return self._hotkey_config

    @hotkey_config.setter
    def hotkey_config(self, new_config: str) -> None:
        """Setter for the hotkey configuration that updates the database and restarts the listener.

        Args:
            new_config (str): The new hotkey configuration from the SystemTrayManager
        """

        if isinstance(new_config, str):
            self._hotkey_config = new_config
            self.db.update_database(
                "hotkeys", "hotkey", new_config, conditions="id = 1"
            )

            if hasattr(self, "listener"):
                self.listener.stop()

            self.setup_hotkey_listener()
        else:
            # TODO: Add error handling - Error Popup would be helpful or screen shake?
            pass

    def setup_hotkey_listener(self) -> None:
        """Set up the key listener with the parsed hotkey."""

        self.hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(self.hotkey_config), self.activate
        )
        self.listener = keyboard.Listener(
            on_press=self.for_canonical(self.hotkey.press),
            on_release=self.for_canonical(self.hotkey.release),
        )
        self.listener.start()

    def setup_enter_listener(self) -> None:
        """Set up the Enter key listener."""

        self.enter_listener = keyboard.Listener(
            on_press=self.on_enter_press,
        )
        self.enter_listener.start()

    def activate(self, key: str = None) -> None:
        """Handle the activation of the hotkey.

        Args:
            key (str): The key that was pressed to activate the hotkey. Not utilized currently
        """

        if self.is_active is True:
            self.show_hide_window.emit()
        else:
            self.is_active = True
            self.hotkey_activated.emit()

    def on_enter_press(self, key) -> None:
        """Handle Enter key press events.

        Args:
            key (str): The key that was pressed. If the key is Enter, emit the enter_key_pressed signal.
        """

        if key == keyboard.Key.enter:
            self.enter_key_pressed.emit()

    def for_canonical(self, f) -> None:
        """Wrapper for canonical key handling.

        Args:
            f: The function to wrap
        """

        return lambda k: f(self.listener.canonical(k))

    # def update_hotkey(self, new_config: str) -> None:
    #     """Update the hotkey configuration and restart the listener.

    #     Args:
    #         new_config (str): The new hotkey configuration from the SystemTrayManager
    #     """

    #     self.db.update_database("hotkeys", "hotkey", f"{new_config}")
    #     self.listener.stop()

    #     # Restart the listener with the new hotkey configuration
    #     self.setup_hotkey_listener()
