from PyQt6.QtWidgets import (
    QPushButton,
    QCheckBox,
    QWidget,
    QTextEdit,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import (
    QTextCursor,
    QColor,
)


class UIFactory(QWidget):
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
    def create_QPushButton(text, callback, object_name=None, width=None, shadow=False):
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
