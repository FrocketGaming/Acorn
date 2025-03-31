from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QLabel,
    QSizePolicy,
    QStyle,
    QToolButton,
)
from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QPalette, QPixmap, QMouseEvent

from src.utils.utils import UtilityManager


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.setObjectName("titleBarLayout")
        self.windows_icon = UtilityManager.get_resource_path("imgs/acorn.ico")
        self.drag_start_pos = None

        # Title Bar Layout
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )

        # Icon Label
        icon_label = QLabel(self)
        icon_label.setObjectName("iconLabel")
        icon_label.setFixedSize(QSize(28, 28))
        icon_pixmap = QPixmap(str(self.windows_icon))
        icon_label.setPixmap(
            icon_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)
        )

        # Title Label
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setText(
            parent.windowTitle()
            if parent.windowTitle()
            else f"{self.__class__.__name__}"
        )

        # Add Icon and Title to Layout
        title_bar_layout.addWidget(icon_label)
        title_bar_layout.addWidget(self.title)

        # Close button
        self.close_button = QToolButton(self)
        self.close_button.setText("X")
        # close_icon = self.style().standardIcon(
            # QStyle.StandardPixmap.SP_TitleBarCloseButton
        # )
        self.close_button.setObjectName("closeButton")
        # self.close_button.setIcon(close_icon)

        self.close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_button.setFixedSize(QSize(28, 28))
        self.close_button.clicked.connect(self.window().close)

        # Add Close Button to Layout
        title_bar_layout.addWidget(self.close_button)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()
            self.window_start_pos = self.window().pos()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if (
            self.drag_start_pos is not None
            and event.buttons() == Qt.MouseButton.LeftButton
        ):
            delta = event.globalPosition().toPoint() - self.drag_start_pos
            self.window().move(self.window_start_pos + delta)
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_start_pos = None
        event.accept()
