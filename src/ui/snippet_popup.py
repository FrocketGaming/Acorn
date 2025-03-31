from PyQt6.QtWidgets import (
    QHBoxLayout,
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QLineEdit,
    QComboBox,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QCursor

from src.ui.ui_factory import UIFactory
from src.ui.title_bar import CustomTitleBar
from src.ui.highlighters.syntax_manager import (
    PythonHighlighter,
    SQLHighlighter,
    HighlighterManager,
)
from src.utils.utils import UtilityManager


class SnippetPopupManager(QDialog):
    closed = pyqtSignal()

    def __init__(self, parent=None, snippet=None, file_extension=None, archived=None):
        super().__init__(parent)
        self.parent = parent
        self.existing_snippet = snippet
        self.extension = file_extension
        self.closed_emitted = False
        self.highlighter_dict = HighlighterManager().highlighters

        # Initialize window properties
        self.setup_window()

        # Initialize tracking variables and timer
        self.setup_tracking()

        # Create and set up the UI components
        self.setup_ui(snippet, archived)

    def setup_window(self):
        """Configure window properties"""
        self.window_icon = UtilityManager.get_resource_path("imgs/acorn.ico")
        self.setWindowTitle("Acorn Snippet Editor")
        self.setWindowIcon(QIcon(str(self.window_icon)))

        # Set window size
        self.min_width = 700
        self.min_height = 400
        self.resize(self.min_width, self.min_height)

        # Set window flags
        self.setWindowFlag(Qt.WindowType.Window)  # Set top-level
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Add offset to the window position
        self.move(self.parent.x() + 120, self.parent.y() + 100)

        # Set dialog object name for styling
        self.setObjectName("Popup")

    def setup_tracking(self):
        """Initialize window move and resize tracking"""
        self.resize_tracking = False
        self.move_tracking = False
        self.last_pos = None

        # Create timer for tracking mouse position
        self.tracking_timer = QTimer(self)
        self.tracking_timer.timeout.connect(self.check_state)
        self.tracking_timer.start(50)  # Check every 50ms

    def setup_ui(self, snippet, archived):
        """Set up the UI layout and components exactly matching original layout"""
        # Main layout setup
        layout = QVBoxLayout()
        title_bar = CustomTitleBar(self)
        title_bar_layout = QVBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.addWidget(title_bar)

        # Main content layout with size grip
        content_layout = QVBoxLayout()
        content_layout.addLayout(layout)

        title_bar_layout.addLayout(content_layout)
        self.setLayout(title_bar_layout)

        # Create each UI section preserving exact layout
        self.create_type_input(layout, snippet, archived)
        self.create_name_input(layout, snippet)
        self.create_description_input(layout, snippet)
        self.create_text_area(layout, snippet)
        self.create_button_area(layout)

    def create_type_input(self, parent_layout, snippet, archived):
        """Create the snippet type input section"""
        type_layout = QHBoxLayout()

        # Type label
        self.type_label = QLabel("Snippet Type:")
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_label.setObjectName("PopupLabel")
        type_layout.addWidget(self.type_label)

        # Type input with extension
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 4, 0)  # Preserve original margins

        # Type input field
        self.type_input = QLineEdit(maxLength=15)
        self.type_input.setObjectName("TypeInputField")

        # Set initial value
        if self.parent.selected_snippet_type and not archived:
            self.type_input.setText(self.parent.selected_snippet_type)
        if snippet:
            self.type_input.setText(snippet["type"])

        # File extension dropdown
        self.file_extension_label = QComboBox()
        self.file_extension_label.addItems(
            [str(ext) for ext in self.parent.snippet_manager.extension_map.values()]
        )
        self.file_extension_label.setObjectName("fileExtensionCombo")

        # Set initial extension
        if self.extension and not snippet:
            self.file_extension_label.setCurrentText(self.extension[0])
        if snippet:
            self.file_extension_label.setCurrentText(snippet["extension"])

        self.file_extension_label.setPlaceholderText("File Ext")
        self.file_extension_label.setFixedWidth(60)

        # Add to layouts - preserve original order
        input_layout.addWidget(self.type_input)
        input_layout.addWidget(self.file_extension_label)
        type_layout.addLayout(input_layout)

        parent_layout.addLayout(type_layout)

    def create_name_input(self, parent_layout, snippet):
        """Create the snippet name input section"""
        snippet_name_layout = QHBoxLayout()

        # Name label
        self.snippet_name_label = QLabel("Snippet Name:")
        self.snippet_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.snippet_name_label.setObjectName("PopupLabel")
        snippet_name_layout.addWidget(self.snippet_name_label)

        # Name input field
        self.snippet_name_input = QLineEdit()
        self.snippet_name_input.setObjectName("InputField")
        if snippet:
            self.snippet_name_input.setText(snippet["name"])

        snippet_name_layout.addWidget(self.snippet_name_input)
        parent_layout.addLayout(snippet_name_layout)

    def create_description_input(self, parent_layout, snippet):
        """Create the description input section"""
        description_layout = QHBoxLayout()

        # Description label
        self.description_label = QLabel("Description:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setObjectName("PopupLabel")
        description_layout.addWidget(self.description_label)

        # Description input field
        self.description_input = QLineEdit()
        self.description_input.setObjectName("InputField")
        if snippet:
            self.description_input.setText(snippet["description"])

        description_layout.addWidget(self.description_input)
        parent_layout.addLayout(description_layout)

    def create_text_area(self, parent_layout, snippet):
        """Create the snippet text area"""
        self.snippet_text_area = QTextEdit(acceptRichText=False)
        self.snippet_text_area.setObjectName("snippetTextArea")
        self.snippet_text_area.setPlaceholderText("Type your snippet here...")

        # Set content if editing existing snippet
        if snippet:
            self.snippet_text_area.setPlainText(snippet.get("content", ""))

            # Apply syntax highlighting for Python files
            extension = snippet.get("extension", "")
            highlighter = self.highlighter_dict.get(extension, None)
            if highlighter:
                self.highlighter = highlighter(self.snippet_text_area.document())

        parent_layout.addWidget(self.snippet_text_area)

    def create_button_area(self, parent_layout):
        """Create the button area with save and close buttons"""
        button_layout = QHBoxLayout()

        # Save button
        self.save_button = UIFactory.create_QPushButton(
            "Save", self.save_snippet, "saveButton", shadow=True
        )
        button_layout.addWidget(self.save_button)

        # Close button
        self.close_button = UIFactory.create_QPushButton(
            "Close", self.close_popup, "closeButton", shadow=True
        )
        button_layout.addWidget(self.close_button)

        parent_layout.addLayout(button_layout)

    def check_state(self):
        """Check for keyboard modifiers and update tracking state"""
        # Get current modifiers
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.KeyboardModifier.ControlModifier)
        shift_pressed = bool(modifiers & Qt.KeyboardModifier.ShiftModifier)

        # Check for Ctrl+Shift (resize mode)
        if ctrl_pressed and shift_pressed and not self.resize_tracking:
            # Start resize tracking
            self.resize_tracking = True
            self.move_tracking = False
            self.last_pos = QCursor.pos()

        # Check for Ctrl only (move mode)
        elif ctrl_pressed and not shift_pressed and not self.move_tracking:
            # Start move tracking
            self.move_tracking = True
            self.resize_tracking = False
            self.last_pos = QCursor.pos()

        # If no modifiers or wrong combination, stop tracking
        elif not ctrl_pressed or (not self.resize_tracking and not self.move_tracking):
            # Stop tracking
            if self.resize_tracking or self.move_tracking:
                self.resize_tracking = False
                self.move_tracking = False
                self.last_pos = None

        # Process mouse movement based on active mode
        if self.resize_tracking:
            self.process_resize()
        elif self.move_tracking:
            self.process_move()

    def process_resize(self):
        """Handle window resizing when in resize mode"""
        current_pos = QCursor.pos()

        if self.last_pos is None:
            self.last_pos = current_pos
            return

        # Calculate delta movement
        dx = current_pos.x() - self.last_pos.x()
        dy = current_pos.y() - self.last_pos.y()

        # Current window size
        width = self.width()
        height = self.height()

        # When mouse moves UP: Height DECREASES (bottom moves up)
        # When mouse moves DOWN: Height INCREASES (bottom moves down)
        # When mouse moves LEFT: Width DECREASES (right side moves left)
        # When mouse moves RIGHT: Width INCREASES (right side moves right)

        # Use the initial size as the minimum
        new_height = max(
            self.min_height, height + dy
        )  # Height changes with vertical mouse movement
        new_width = max(
            self.min_width, width + dx
        )  # Width changes with horizontal mouse movement

        # Resize window
        self.resize(new_width, new_height)

        # Update last position
        self.last_pos = current_pos

    def process_move(self):
        """Handle window movement when in move mode"""
        current_pos = QCursor.pos()

        if self.last_pos is None:
            self.last_pos = current_pos
            return

        # Calculate movement delta
        dx = current_pos.x() - self.last_pos.x()
        dy = current_pos.y() - self.last_pos.y()

        # Current window position
        x = self.x()
        y = self.y()

        # New position
        new_x = x + dx
        new_y = y + dy

        # Move window
        self.move(new_x, new_y)

        # Update last position
        self.last_pos = current_pos

    def close_popup(self):
        if not self.closed_emitted:
            self.closed.emit()  # Emit closed signal
            self.closed_emitted = True  # Set flag to prevent further emissions
        self.close()

    def delete_snippet(self):
        self.parent.snippet_manager.delete_snippet(self.existing_snippet)
        self.snippet_changed.emit()
        self.close()

    def save_snippet(self):
        # Retrieve input values
        snippet_name = self.snippet_name_input.text()
        snippet_type = self.type_input.text()
        description = self.description_input.text()
        snippet_content = self.snippet_text_area.toPlainText()
        snippet_extension = self.file_extension_label.currentText()

        # Create the new snippet entry
        new_snippet = {
            "Name": f"""{snippet_name}""",
            "Type": f"""{snippet_type}""",
            "Description": f"""{description}""",
            "Content": f"""{snippet_content}""",
            "Extension": f"""{snippet_extension}""",
        }

        if self.existing_snippet is None:
            self.parent.snippet_manager.save_snippet(new_snippet)
        else:
            self.parent.snippet_manager.update_existing_snippet(
                new_snippet, self.existing_snippet
            )
        self.parent.selected_snippet_type = snippet_type
        self.parent.snippets_refreshed = True
        self.parent.refresh_app()
        self.close()

    def closeEvent(self, event):
        if not self.closed_emitted:
            self.closed.emit()
            self.closed_emitted = True
        event.accept()
