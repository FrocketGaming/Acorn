import os
import sys
from pathlib import Path
from src import (
    KeyboardManager,
    SystemTrayManager,
    QtManager,
    ConfigurationManager,
    UpdateManager,
    PopupManager,
)
from PyQt6.QtWidgets import QApplication


def app():
    """
    Entry point of the application.

    Creates a QApplication, configures the ConfigurationManager, instantiates the
    KeyboardManager, QtManager, and SystemTrayManager, and starts the event loop.

    Returns:
        None
    """
    app = QApplication(sys.argv)
    update_handler = UpdateManager()
    ConfigurationManager()
    kb_handler = KeyboardManager()

    qt_handler = QtManager(kb_handler, update_handler)
    SystemTrayManager(qt_handler, kb_handler)

    qt_handler.show_window()

    # Start the event loop and prevent the application from closing when the main window is closed
    # TODO: Reactivate this and update the CURRENT_VERISON to 0.3.0
    app.setQuitOnLastWindowClosed(False)
    app.exec()


if __name__ == "__main__":
    # Add the project root directory to Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))

    # Set the working directory to the project root
    os.chdir(project_root)

    app()
