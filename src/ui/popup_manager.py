from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.ui.snippet_popup import SnippetPopupManager
from src.ui.title_bar import CustomTitleBar


class PopupManager:
    @staticmethod
    def create_snippet_popup(parent=None, snippet=None, file_extension=None):
        """
        Creates the popup window when editing or creating new snippets for the application.

        Args:
            parent: Parent class
            snippet: Dictionary of snippet content to be edited.
            file_extension: File extension for filling the combobox should it be a new snippet that does not have these values.

        Returns:
            QDialog Object
        """
        popup = SnippetPopupManager(
            parent=parent, snippet=snippet, file_extension=file_extension
        )
        return popup

    @staticmethod
    def create_generic_popup(
        parent=None, title="Popup", icon_path=None, window_size=(700, 400), message=None
    ) -> QDialog:
        """
        Create a generic popup for the handling of error messages and any additionally required popups.

        Args:
            parent: Parent class
            title: Header for the popup window
            icon_path: Path for the icon to be displayed should it change
            window_size: Defaulted to 700x400
            message: Content to be displayed within the popup window.

        Returns:
            QDialog object.
        """

        # TODO: Window size should be responsive to the content especially for errors.
        popup = QDialog(parent)
        popup.setWindowTitle(title)
        popup.setWindowFlag(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        if icon_path:
            popup.setWindowIcon(QIcon(str(icon_path)))
        popup.setFixedSize(QSize(*window_size))

        # Main layout for the popup
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title_bar = CustomTitleBar(popup)
        layout.addWidget(title_bar)

        # Content layout
        content_layout = QVBoxLayout()

        # Add a QTextEdit to show the message
        details = QTextEdit()
        if message:
            details.setText(message)
        details.setReadOnly(True)  # Make it read-only for viewing purposes
        content_layout.addWidget(details)

        # Optionally add a Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(popup.accept)
        content_layout.addWidget(close_button)

        # Add content layout to main layout
        layout.addLayout(content_layout)

        popup.setLayout(layout)
        popup.setObjectName("Popup")
        return popup
