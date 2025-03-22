colors = {
    "background": "#282a36",
    "current_line": "#1d1e27",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c",
    "palette": {
        "Window": "background",
        "WindowText": "foreground",
        "Base": "background",
        "AlternateBase": "current_line",
        "ToolTipBase": "background",
        "ToolTipText": "foreground",
        "Text": "foreground",
        "Button": "purple",
        "ButtonText": "background",
        "Highlight": "pink",
        "HighlightedText": "background",
    },
}

qss = """
    QMainWindow, QWidget {{
        background-color: {background};
    }}
    QVBoxLayout {{
        padding: 0px;
        margin: 0px;
    }}
    QHBoxLayout {{
        padding: 2px;
        margin: 0px;
    }}
    QMenu {{
        background-color: {background};
        color: {foreground};
        text-align: center; 
        max-width: 150px;
    }}
    QMenu::item:selected {{
        background-color: {current_line};
        color: {foreground};
    }}
    QVBoxLayout {{
        padding: 0px;
        margin: 0px;
    }}
    QTextEdit {{
        background-color: {background};
        color: {foreground};
        border: 1px solid {comment};
        font-size: 16px;
        text-align: AlignCenter;
    }}
    QScrollArea QPushButton {{
        background-color: {background};
        color: {foreground};
        border-radius: 10px;
        border: 1px solid {green};
    }}
    QPushButton {{
        background-color: {purple};
        color: {background};
        border: none;
        padding: 5px;
        min-width: 80px;
    }}
    QPushButton:hover {{
        background-color: {pink};
    }}
    QToolTip {{
        background-color: {background};
        color: {foreground};
        border: 1px solid {comment};
        padding: 5px;
    }}
    QTextEdit {{
        background-color: {background};
        color: {foreground};
        border: 1px solid {comment};
        font-size: 16px;
        text-align: AlignCenter;
    }}
    QLabel {{
        color: {foreground};
        font-weight: bold;
    }}
    QLineEdit {{
        background-color: {background};
        color: {foreground};
        border: 1px solid {orange};
        text-align: AlignCenter;
    }}
    #Container {{
        background: {background};
        border-radius: 10px; 
    }}
    #titleBarLayout #iconLabel {{
        background-color: {pink};
        padding-left: 10px;
        color: {foreground};
    }}
    #titleBarLayout QWidget {{
        background-color: {pink};
        color: {current_line};
        margin: 0px;
        padding: 0px;
        font-weight: bold;
    }}
    #titleBarLayout #closeButton {{
        background-color: {pink};
        margin: 0px;
        border: none;
    }}
    #titleBarLayout #closeButton:hover {{
        background-color: {red};
        border: none;
    }}
    #typeWidget {{
        margin: 0px;
        padding: 0px;
    }}
    #contentScrollArea {{
        background-color: {current_line};
        border: 1px solid {comment};
        margin: 0px 4px 0px 4px;
    }}
    #contentWidget {{
        background-color: {current_line};
        padding: 0px;
    }}
    #typeButton {{
        background-color: {background};
        color: {foreground};
        border: 1px solid {current_line};
        padding: 5px;
        min-width: 80px;
    }}
    #typeButton:hover {{
        font: bold;
        color: {pink};
    }}
    #typeButton:focus {{
        background-color: {orange};
        color: {background};
        font: bold;
        border: none;
        padding: 5px;
        min-width: 80px;
    }}
    #searchBar {{
        border: 1px solid {orange};
        padding-left: 5px;
        margin-left: 4px;
    }}
    #searchButton {{
        background-color: {purple};
        color: {background};
        border: 1px solid {comment};
    }}
    #searchButton:hover {{
        background-color: {pink};
    }}
    #clearButton {{
        background-color: {background};
        color: {foreground};
        margin: 0px 4px 0px 0px;
    }}
    #copyButton {{
        background-color: {green};
        color: {background};
        border: 1px solid {current_line};
    }}
    #createButton {{
    }}
    #editButton {{
        background-color: {pink};
        color: {background};
        border: 1px solid {comment};
        min-width: 20px;
    }}
    #editButton QToolTip {{
        background-color: {current_line};
        color: {pink};
        border: 1px solid {green};
        padding: 0px;
        margin: 0px;
    }}
    #editButton:hover {{
        background-color: {cyan};
    }}
    #deleteButton {{
        background-color: {red};
        color: {background};
        border: 1px solid {comment};
        min-width: 15px;
        min-height: 5px;
    }}
    #deleteButton QToolTip {{
        background-color: {current_line};
        color: {red};
        border: 1px solid {comment};
        padding: 0px;
        margin: 0px;
    }}
    #deleteButton:hover {{
        background-color: {pink};
    }}
    #themePicker {{
        color: #ffffff;
        background-color: {current_line};
        border: None;
        text-align: center;
    }}
    QComboBox QAbstractItemView {{
        background-color: {current_line};
        color: {foreground};
    }}
    """
