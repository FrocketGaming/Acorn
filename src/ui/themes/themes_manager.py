from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QTextEdit
from src.ui.themes import acorn, dracula, matcha, matchav2
from src.data.database_manager import DatabaseManager
from src.ui.highlighters.syntax_manager import PythonHighlighter
from typing import Dict


class ThemeManager:
    _current_theme = None

    def __init__(self):
        self.themes = {theme.name: theme for theme in all_themes}
        self.highlighters = []
        default_theme = self.get_default_theme()
        self.current_theme = default_theme

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @current_theme.setter
    def current_theme(self, theme_name: str) -> None:
        """Set and apply the selected theme to the application.

        Args:
            theme_name (str): The name of the theme to apply.
        """
        self.apply_theme(theme_name)

    def apply_theme(self, theme_name: str) -> None:
        """Apply the selected theme to the application.

        Args:
            theme_name (str): The name of the theme to apply.
        """

        if theme_name in self.themes:
            self._current_theme = self.themes[theme_name]
            self._current_theme.apply()

        for highlighter in self.highlighters:
            highlighter.refresh_theme()

    def get_theme_names(self) -> Dict:
        return list(self.themes.keys())

    def get_default_theme(self) -> str:
        """Get the default theme from the database"""
        default_theme = DatabaseManager().read_database(
            "default_theme", "theme", conditions="id = 1"
        )
        return default_theme["theme"][0]

    def update_default_theme(self, theme_name: str) -> None:
        """Update the default theme in the database"""
        DatabaseManager().update_database(
            "default_theme", "theme", theme_name, conditions="id = 1"
        )

    def get_theme_color(self, role: str) -> QColor:
        """Retrieve color from the current theme's palette."""
        if self._current_theme:
            return self._current_theme.get_theme_color(role)
        return QColor()


class Theme:
    def __init__(self, name: str, colors: Dict, stylesheet: str):
        self.name = name
        self.colors = colors
        self.stylesheet = stylesheet

    def apply(self) -> None:
        """Apply the theme to the application."""

        formatted_stylesheet = self.stylesheet.format(**self.colors)
        QApplication.instance().setStyleSheet(formatted_stylesheet)
        self.set_palette()

    def set_palette(self) -> None:
        """Set the color palette for the application."""

        palette = QApplication.instance().palette()
        for role, color_name in self.colors["palette"].items():
            color_value = self.colors[color_name]
            palette.setColor(getattr(QPalette.ColorRole, role), QColor(color_value))
        QApplication.instance().setPalette(palette)

    def get_theme_color(self, role: str) -> QColor:
        """Retrieve color from the current theme's palette."""
        color_name = self.colors["palette"].get(role, None)
        if color_name:
            color_value = self.colors[color_name]
            return QColor(color_value)
        return QColor()


# Define themes

all_themes = [
    Theme("Acorn", acorn.colors, acorn.qss),
    # Theme("Dracula", dracula.colors, dracula.qss),
    Theme("Matcha", matcha.colors, matcha.qss),
    # Theme("Matcha V2", matchav2.colors, matchav2.qss),
]
