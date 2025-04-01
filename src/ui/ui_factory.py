from PyQt6.QtWidgets import (
    QPushButton,
    QCheckBox,
    QWidget,
    QTextEdit,
    QGraphicsDropShadowEffect,
    QMenu,
    QLabel,
)
from PyQt6.QtGui import QTextCursor, QColor, QAction
from PyQt6.QtCore import Qt


class UIFactory(QWidget):
    def __init__(self):
        super().__init__()

    @staticmethod
    def show_context_menu(button, position, context_menu):
        """
        Display a context menu at the given position.

        Args:
            button: The button that triggered the context menu
            position: The position where to show the menu
            context_menu: Dictionary with menu items as keys and callbacks as values
        """
        menu = QMenu(button)
        menu.setObjectName("contextMenu")

        # Add each action from the dictionary
        for action_text, action_callback in context_menu.items():
            action = QAction(action_text, button)
            action.triggered.connect(action_callback)
            menu.addAction(action)
        # Show the menu
        menu.exec(button.mapToGlobal(position))

    @staticmethod
    def create_QCheckBox(text, callback=None, checked=False, object_name=None):
        """Generic create checkbox factory method."""

        checkbox = QCheckBox(text)
        if callback:
            checkbox.stateChanged.connect(callback)
        if checked:
            checkbox.setChecked(True)
        if object_name:
            checkbox.setObjectName(object_name)
        return checkbox

    @staticmethod
    def create_QPushButton(
        text, callback, object_name=None, width=None, shadow=False, context_menu=None
    ):
        """Generic create button factory method."""

        button = QPushButton(text)
        if callback:
            button.clicked.connect(callback)
        if object_name:
            button.setObjectName(object_name)
        if width:
            button.setFixedWidth(width)
        if shadow:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            shadow.setXOffset(0.1)
            shadow.setYOffset(0.5)
            shadow.setColor(QColor(0, 0, 0, 200))
            button.setGraphicsEffect(shadow)
        if context_menu:
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

            # Connect the context menu signal to a lambda that calls show_context_menu
            button.customContextMenuRequested.connect(
                lambda pos: UIFactory.show_context_menu(button, pos, context_menu)
            )
        return button

    @staticmethod
    def create_QTextarea(
        text, tooltip=None, object_name=None, read_only=False, fixed_height=None
    ):
        text_area = QTextEdit()
        text_area.setPlainText(text)
        if tooltip:
            if len(tooltip) > 400:
                text_area.setToolTip(tooltip[:400] + "\n...")
            else:
                text_area.setToolTip(tooltip)
        if object_name:
            text_area.setObjectName(object_name)
        if read_only:
            text_area.setReadOnly(True)
        if fixed_height:
            text_area.setFixedHeight(fixed_height)

        cursor = text_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        text_area.setTextCursor(cursor)
        text_area.ensureCursorVisible()
        return text_area

    @staticmethod
    def create_QLabel(
        text, tooltip=None, object_name=None, read_only=False, fixed_height=None
    ):
        label = QLabel(text)
        label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )  # Allow text selection

        if tooltip:
            label.setToolTip(tooltip[:400] + "\n..." if len(tooltip) > 400 else tooltip)

        if object_name:
            label.setObjectName(object_name)

        if fixed_height:
            label.setFixedHeight(fixed_height)

        return label
