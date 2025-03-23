from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.ui.snippet_popup import SnippetPopupManager
from src.ui.title_bar import CustomTitleBar
from src.ui.ui_factory import UIFactory


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
        parent=None,
        title="Popup",
        icon_path=None,
        window_size=(700, 400),
        message=None,
        **kwargs,
    ) -> QDialog:
        """
        Create a generic popup for the handling of error messages and any additionally required popups.

        Args:
            parent: Parent class
            title: Header for the popup window
            icon_path: Path for the icon to be displayed should it change
            window_size: Defaulted to 700x400
            message: Content to be displayed within the popup window.
            **kwargs: Additional parameters:
                - close_button_text: Text to display on the close button (default: "Close")
                - additional_button: Text for an additional button (e.g. "Delete")
                - label_object_name: Object name for the message label
                - btn_object_name: Object name for the additional button

        Returns:
            QDialog object.
        """
        # Parse kwargs with defaults
        close_button_txt = kwargs.get("close_button_txt", "Close")
        additional_button = kwargs.get("additional_button", None)
        label_object_name = kwargs.get("label_object_name", None)
        btn_object_name = kwargs.get("btn_object_name", None)
        close_object_name = kwargs.get("close_object_name", None)

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

        details = QLabel()
        details.setObjectName(label_object_name)

        if message:
            details.setText(message)
        content_layout.addWidget(details)

        button_layout = QHBoxLayout()

        if additional_button:
            additional_button = UIFactory.create_QPushButton(
                additional_button, None, btn_object_name, shadow=True
            )
            additional_button.clicked.connect(popup.accept)
            button_layout.addWidget(additional_button)

        close_button = UIFactory.create_QPushButton(
            close_button_txt, None, close_object_name, shadow=True
        )
        close_button.clicked.connect(popup.reject)

        button_layout.addWidget(close_button)

        layout.addLayout(content_layout)
        layout.addLayout(button_layout)
        popup.setLayout(layout)
        popup.setObjectName("Popup")
        return popup
