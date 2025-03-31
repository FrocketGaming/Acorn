from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QApplication,
    QScrollArea,
    QToolTip,
    QLabel,
    QLineEdit,
    QComboBox,
    QDialog,
    QStyle,
    QPushButton,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QIcon, QBrush, QFont, QTextCharFormat, QCursor

from src.ui.themes.themes_manager import ThemeManager
from src.ui.title_bar import CustomTitleBar

# from src.ui.snippet_popup import SnippetPopupManager
from src.ui.popup_manager import PopupManager
from src.ui.ui_factory import UIFactory
from src.data.snippet_manager import SnippetManager
from src.utils.utils import UtilityManager
from functools import partial

import arrow


class UIConstants:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_icon = UtilityManager.get_resource_path("imgs/acorn.ico")
        self._setup_base_window()

    def _setup_base_window(self):
        """Setup basic window properties common to all windows"""
        self.setWindowTitle("Acorn")
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon(str(self.window_icon)))

        # Get the screen resolution
        screen = self.screen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Apply the fixed window size
        self.setFixedSize(UIConstants.WINDOW_WIDTH, UIConstants.WINDOW_HEIGHT)

        # Ensure it doesn't exceed screen bounds
        self.setGeometry(
            (screen_width - UIConstants.WINDOW_WIDTH) // 2,
            (screen_height - UIConstants.WINDOW_HEIGHT) // 2,
            UIConstants.WINDOW_WIDTH,
            UIConstants.WINDOW_HEIGHT,
        )

    def create_main_widget(self) -> QWidget:
        """Create and return the main widget with basic setup"""
        main_widget = QWidget()
        main_widget.setFont(QFont("Helvetica", 10))
        main_widget.setObjectName("Container")
        return main_widget

    def create_base_layout(self) -> tuple[QVBoxLayout, QVBoxLayout]:
        """Create and return the basic layouts for the window"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)

        title_bar_layout = QVBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return main_layout, title_bar_layout

    def show_window(self):
        """Show and activate the window"""
        self.show()
        self.raise_()
        self.activateWindow()


class QtManager(BaseWindow):
    def __init__(self, kb_handler, updater):
        super().__init__()
        self.selected_snippet_type = None
        self._initalize_managers(kb_handler, updater)
        self.ui = UIComponents(self, updater)
        self.ui._setup_main_ui()
        self.keyboard_manager.show_hide_window.connect(self.show_hide_window)
        self.keyboard_manager.enter_key_pressed.connect(
            self.search_manager.perform_search
        )
        self.default_view = False
        self.snippets_refreshed = False

    def _initalize_managers(self, kb_handler, updater):
        self.keyboard_manager = kb_handler
        self.update_manager = updater
        self.snippet_manager = SnippetManager()
        self.theme_manager = ThemeManager()
        self.content_manager = ContentManager(
            self,
            self.snippet_manager,
            self.theme_manager,
        )
        self.search_manager = SearchManager(self)

    def show_hide_window(self):
        """Show or hide the main application window based on its current state."""
        if self.isVisible():
            self.ui.search_bar.clearFocus()
            self.hide()
        else:
            # Get the current cursor position
            cursor_pos = QCursor.pos()

            # Show the window first
            self.show()

            # Center the window on the cursor position
            window_width = self.width()
            window_height = self.height()

            # Calculate the top-left position that would center the window on cursor
            x_pos = cursor_pos.x() - (window_width // 2)
            y_pos = cursor_pos.y() - (window_height // 2)

            # Move the window to the calculated position
            self.move(x_pos, y_pos)

            # Bring window to front and focus it
            self.raise_()
            self.activateWindow()

    def missing_schema_default_layout(self, parent_layout):
        label = QLabel("No snippets found, please create your first snippet")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px")
        parent_layout.addWidget(label)

    def refresh_app(self, archived=False):
        """Re-focus the selected snippet type button after a snippet is created or edited."""
        self.ui._setup_main_ui(archived)

        if (
            self.selected_snippet_type is not None
            and self.selected_snippet_type
            in self.snippet_manager.get_snippet_types(archived)
        ):
            button = self.ui.active_buttons[self.selected_snippet_type]
            button.setFocus()
            button.click()

    # TODO: Move to ClipboardManager
    def copy_to_clipboard(self, text):
        """Copy the snippet content to the clipboard and show a tooltip."""

        QApplication.clipboard().setText(text)

        button = self.sender()
        button_pos = button.mapToGlobal(button.rect().center())
        QToolTip.showText(button_pos, "Copied!", button)
        QTimer.singleShot(1500, QToolTip.hideText)


class ContentManager:
    def __init__(self, parent, snippet_manager, theme_manager):
        self.parent = parent
        self.popup = None
        self.snippet_manager = snippet_manager
        self.theme_manager = theme_manager
        self.search_results = []
        self.copy_icon = UtilityManager.get_resource_path("imgs/copy-solid.svg")
        self.edit_icon = UtilityManager.get_resource_path("imgs/edit.png")
        self.file_extension = None
        self.archived = None
        self.archive_status = False
        self.check_current_release()

    def clear_search(self):
        self.parent.ui.search_bar.clear()

    def clear_content(self):
        """Clear the search bar and search results, and remove all snippets from the content area."""

        self.clear_layout(self.parent.ui.content_layout)

    def clear_layout(self, layout):
        """Clear the layout of all widgets."""

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    # TODO:
    # def edit_snippet(self):
    # self.snippet_manager.edit_in_vscode(snippet_id)

    def create_and_edit_snippet_popup(self, snippet=None):
        if not hasattr(self, "popup") or self.popup is None:
            self.popup = PopupManager.create_snippet_popup(
                self.parent,
                snippet,
                self.file_extension,
                self.archived,
            )
            self.popup.closed.connect(self.on_popup_closed)
            self.popup.show()

    def on_popup_closed(self):
        if self.popup:
            self.popup = None

            if not self.parent.snippets_refreshed:
                self.display_snippets(self.parent.selected_snippet_type)
            self.parent.snippets_refreshed = False

    def display_snippets(self, snippet_type=None, search_results=None):
        """Display snippets based on the snippet_type selected or search results."""

        self.parent.selected_snippet_type = snippet_type
        # self.archived = self.snippet_manager.check_archive_status(snippet_type)

        self.clear_content()

        filtered_content = search_results or self.parent.snippet_manager.get_snippets(
            snippet_type, archived=self.archive_status
        )

        self.file_extension = sorted(
            [str(item["extension"]) for item in filtered_content]
        )

        sorted_content = sorted(filtered_content, key=lambda x: x["name"])

        for item in sorted_content:
            row_layout = QHBoxLayout()

            text_area = UIFactory.create_QTextarea(
                text="",
                tooltip=item["content"],
                object_name="SnippetTextArea",
                read_only=True,
            )
            text_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            cursor = text_area.textCursor()

            # Set name to bold and larger font
            name_format = QTextCharFormat()
            name_format.setForeground(
                QBrush(self.parent.theme_manager.get_theme_color("Highlight"))
            )
            name_format.setFontWeight(QFont.Weight.Bold)
            name_format.setFontPointSize(14)
            cursor.insertText(item["name"], name_format)

            # Insert separator and description in a smaller font
            desc_format = QTextCharFormat()
            desc_format.setFontPointSize(12)

            cursor.insertText(": " + item["description"], desc_format)

            text_area.setTextCursor(cursor)  # Apply the styled text

            copy_button = UIFactory.create_QPushButton(
                "",
                partial(self.parent.copy_to_clipboard, item["content"]),
                "copyButton",
                shadow=True,
            )
            copy_button.setIcon(QIcon(str(self.copy_icon)))
            copy_button.setToolTip("Copy Snippet")

            # TODO: Add back for VsCode support
            edit_button = UIFactory.create_QPushButton(
                "",
                partial(
                    # self.snippet_manager.edit_in_vscode,
                    self.parent.content_manager.create_and_edit_snippet_popup,
                    snippet=item,
                    # snippet_id=item["id"],
                ),
                "editButton",
                shadow=True,
            )
            edit_button.setIcon(QIcon(str(self.edit_icon)))
            edit_button.setToolTip("Edit Snippet")

            delete_button = UIFactory.create_QPushButton(
                "X",
                partial(self.delete_snippet, item),
                "deleteButton",
                shadow=True,
            )
            delete_button.setToolTip("Delete Snippet")

            row_layout.addWidget(delete_button)
            row_layout.addWidget(text_area)
            row_layout.addWidget(copy_button)
            row_layout.addWidget(edit_button)

            self.parent.ui.content_layout.addLayout(row_layout)
            self.parent.ui.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def delete_snippet(self, snippet):
        popup = PopupManager.create_generic_popup(
            parent=self.parent,
            title="Confirm Deletion",
            window_size=(200, 100),
            message="Delete Snippet?",
            close_button_txt="No",
            additional_button="Yes",
            message_object_name="deleteConfirmationLabel",
            btn_object_name="deleteConfirmationButton",
            close_object_name="deleteConfirmationCloseButton",
        )

        popup.show()
        result = popup.exec()
        if result == QDialog.DialogCode.Accepted:
            self.snippet_manager.delete_snippet(snippet["id"])
        self.parent.refresh_app()

    def check_current_release(self):
        db_version = self.snippet_manager.db_release.item()
        if db_version != self.parent.update_manager.latest_version:
            self.display_release_notes(db_version)

    def display_release_notes(self, db_version: str = None):
        popup = PopupManager.create_generic_popup(
            parent=self.parent,
            title="Release Notes",
            window_size=(700, 400),
            message=self.parent.update_manager.get_release_notes(),
            auto_size=True,
            is_markdown=True,
        )
        popup.show()

        if db_version:
            if db_version != self.parent.update_manager.get_current_version():
                print("Updating release in database")
                self.update_release_in_db()

    def update_release_in_db(self):
        self.snippet_manager.db.update_database(
            table_name="release",
            columns=["release", "lst_updt_ts"],
            values=(
                self.parent.update_manager.get_current_version(),
                arrow.now().format("YYYY-MM-DD"),
            ),
        )


class SearchManager:
    def __init__(self, parent):
        self.parent = parent

    def perform_search(self):
        """Search for snippets based on the query in the search bar."""

        if self.parent.isActiveWindow() and self.parent.isVisible():
            if self.parent.default_view is False:
                query = self.parent.ui.search_bar.text()
                self.search_results = self.parent.snippet_manager.perform_search(
                    query, archived_status=self.parent.content_manager.archive_status
                )
                self.parent.content_manager.clear_content()
                if self.search_results:
                    self.parent.content_manager.display_snippets(
                        search_results=self.search_results
                    )
                else:
                    label = QLabel("No snippets found")
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setStyleSheet("font-size: 18px")
                    self.parent.ui.content_layout.addWidget(label)


class UIComponents:
    """Handles UI component creation and layout"""

    def __init__(self, parent, updater):
        self.parent = parent
        self.update_manager = updater

    def _setup_main_ui(self, archived=False):
        """Setup the main UI structure"""
        self.archive_status = archived
        main_widget = self._create_main_widget()
        main_layout, title_bar_layout = self._create_base_layout()

        self.parent.title_bar = CustomTitleBar(self.parent)
        title_bar_layout.addWidget(self.parent.title_bar)
        title_bar_layout.addLayout(main_layout)

        self._setup_ui_elements(main_layout)

        main_widget.setLayout(title_bar_layout)
        self.parent.setCentralWidget(main_widget)

    def _create_main_widget(self):
        """Create the main widget with basic setup"""
        main_widget = QWidget()
        main_widget.setFont(QFont("Helvetica", 10))
        main_widget.setObjectName("Container")
        return main_widget

    def _create_base_layout(self):
        """Create the base layouts"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)

        title_bar_layout = QVBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return main_layout, title_bar_layout

    def _setup_ui_elements(self, main_layout, archived=False):
        """Setup all UI elements"""
        main_elements = [
            self.add_theme_picker,
            self.add_search_bar,
            self.add_type_buttons,
            self.add_content_area,
            self.archive_and_release_notes,
            self.create_snippets_button,
        ]

        if not self.parent.snippet_manager.get_snippets(columns="id"):
            self.parent.default_view = True
            self.parent.missing_schema_default_layout(main_layout)
            self.create_snippets_button(main_layout)
        else:
            for element in main_elements:
                element(main_layout)

    # TODO: Move to a better place
    def update_app(self):
        self.update_text.clear()
        self.update_button.setHidden(True)
        QTimer.singleShot(1500, self.update_manager.update())

    def add_theme_picker(self, parent_layout):
        """Add a combo box to select the theme to the main layout."""

        layout = QHBoxLayout()
        layout.setObjectName("themeLayout")

        if self.update_manager.update_required:
            self.update_text = QLabel(
                f"v{self.update_manager.latest_version} is available!"
            )
            self.update_text.setObjectName("updateLabel")
            self.update_button = UIFactory.create_QPushButton(
                "Download", self.update_app, "updateButton"
            )
            layout.addWidget(self.update_text)
            layout.addWidget(self.update_button)

        self.theme_picker_combo = QComboBox()
        self.theme_picker_combo.addItems(self.parent.theme_manager.get_theme_names())
        self.theme_picker_combo.setFixedWidth(90)
        self.theme_picker_combo.setObjectName("themePicker")
        self.theme_picker_combo.currentTextChanged.connect(
            self.parent.theme_manager.apply_theme
        )

        self.theme_picker_combo.setCurrentText(
            self.parent.theme_manager.current_theme.name
        )

        layout.addStretch()
        layout.addWidget(self.theme_picker_combo)
        layout.setContentsMargins(0, 0, 5, 0)
        parent_layout.addLayout(layout)

    def add_content_area(self, parent_layout):
        """Add a scrollable area to display the snippets, but remove it if no snippets are found."""

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("contentScrollArea")

        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")

        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setObjectName("contentLayout")

        scroll_area.setWidget(self.content_widget)
        parent_layout.addWidget(scroll_area)

    def add_search_bar(self, parent_layout):
        """Add a search bar to the main layout to filter snippets."""

        layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search snippets...")
        self.search_bar.setFixedHeight(35)
        self.search_bar.setObjectName("searchBar")

        search_btn = UIFactory.create_QPushButton(
            "Search",
            self.parent.search_manager.perform_search,
            "searchButton",
            shadow=True,
        )
        clear_btn = UIFactory.create_QPushButton(
            "Clear",
            self.parent.content_manager.clear_search,
            "clearButton",
            shadow=True,
        )

        layout.addWidget(self.search_bar)
        layout.addWidget(search_btn)
        layout.addWidget(clear_btn)
        parent_layout.addLayout(layout)

    def create_text_area(self, text):
        """Create the text area to display snippet information."""

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText(str(text))
        text_area.setFixedHeight(35)
        text_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cursor = text_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        text_area.setTextCursor(cursor)
        text_area.ensureCursorVisible()
        return text_area

    def archive_state_change(self, state):
        if state == 2:  # Checked
            self.parent.content_manager.archive_status = True
            self.parent.refresh_app(archived=True)
        else:
            self.parent.content_manager.archive_status = False
            self.parent.refresh_app(archived=False)

    def archive_and_release_notes(self, parent_layout):
        layout = QHBoxLayout()

        # Create checkbox only if it doesn't already exist
        if not hasattr(self, "archive_checkbox"):
            # Create checkbox if it doesn't exist
            self.archive_checkbox = UIFactory.create_QCheckBox(
                text="View Archived Snippets",
                callback=self.archive_state_change,
                checked=self.parent.content_manager.archive_status,
                object_name="archiveCheckbox",
            )

        # Create icon button if it doesn't exist
        if not hasattr(self, "icon_button"):
            icon_button = QPushButton("?")
            icon_button.setObjectName("releaseNotesButton")
            icon_button.clicked.connect(
                self.parent.content_manager.display_release_notes
            )

            self.icon_button = icon_button  # Store reference to the icon button

        # Add the checkbox and icon button to the layout
        layout.addWidget(self.archive_checkbox)
        layout.addStretch()  # Pushes the next widget (icon button) to the right
        layout.addWidget(self.icon_button)

        parent_layout.addLayout(layout)

    def create_snippets_button(self, parent_layout):
        """Add buttons to create and edit snippets to the main layout."""

        layout = QHBoxLayout()
        create_button = UIFactory.create_QPushButton(
            "Create Snippet",
            partial(
                self.parent.content_manager.create_and_edit_snippet_popup,
                snippet=None,
            ),
            "createButton",
            shadow=True,
        )
        layout.addWidget(create_button)
        parent_layout.addLayout(layout)

    def archive_snippet_type(self, snippet_type: str) -> None:
        self.parent.snippet_manager.archive_snippet_type(snippet_type)
        self.parent.refresh_app()

    def add_type_buttons(self, parent_layout):
        """Add buttons to filter snippets by snippet_type to the main layout. Remove them if no snippets are found."""
        self.active_buttons = {}

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(55)
        scroll_area.setObjectName("typeScrollArea")

        button_widget = QWidget()
        button_widget.setObjectName("typeWidget")

        button_layout = QHBoxLayout(button_widget)

        for snippet_type in self.parent.snippet_manager.get_snippet_types(
            self.archive_status
        ):
            # Create a function that returns the lambda for the context menu
            def make_archive_action(type_name):
                return lambda: self.archive_snippet_type(type_name)

            # Create a function that returns the lambda for the button click
            def make_display_action(type_name):
                return lambda: self.parent.content_manager.display_snippets(type_name)

            if self.parent.content_manager.archive_status:
                button = UIFactory.create_QPushButton(
                    snippet_type,
                    make_display_action(
                        snippet_type
                    ),  # Use the function to create the click callback
                    "typeButtonArchived",
                    shadow=True,
                )
            else:
                # Create the button with the specific actions for this snippet_type
                button = UIFactory.create_QPushButton(
                    snippet_type,
                    make_display_action(
                        snippet_type
                    ),  # Use the function to create the click callback
                    "typeButton",
                    shadow=True,
                    context_menu={
                        "Archive": make_archive_action(
                            snippet_type
                        )  # Use the function to create the menu callback
                    },
                )

            self.active_buttons[snippet_type] = button

            button_layout.addWidget(button)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            button_layout.setContentsMargins(10, 10, 10, 0)

        scroll_area.setWidget(button_widget)

        # Make the scroll bar appear only horizontally
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        parent_layout.addWidget(scroll_area)
