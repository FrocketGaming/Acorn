colors = {
    "background": "#2C241D",
    "border": "#372C23",
    "foreground": "#36312c",
    "current_line": "#413b35",
    "green": "#c2eabd",
    "yellow": "#fabc23",
    "red": "#ac472f",
    "white": "#ffffff",
    "rose": "#fae3e3",
    "palette": {
        "Window": "background",
        "WindowText": "foreground",
        "Base": "background",
        "AlternateBase": "background",
        "ToolTipBase": "background",
        "ToolTipText": "foreground",
        "Text": "red",
        "Button": "red",
        "ButtonText": "background",
        "Highlight": "red",
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
#Container {{
		background: {background};
		border-radius: 10px; 
}}
#titleBarLayout #iconLabel {{
    background-color: {yellow};
    padding-left: 10px;
    color: {white};
}}
#titleBarLayout QWidget {{
    background-color: {yellow};
    color: {background};
    margin: 0px;
    padding: 0px;
    font-weight: bold;
}}
#titleBarLayout #closeButton {{
    background-color: {yellow};
    margin: 0px;
    border: none;
}}
#titleBarLayout #closeButton:hover {{
    background-color: {yellow};
    border: none;
}}
#typeScrollArea {{
}}
#typeWidget {{
    margin: 0px;
    padding: 0px;
}}
#contentScrollArea {{
    background-color: {background};
    border: 1px solid {border};
    border-radius: 5px;
}}
#contentWidget {{
    background-color: {foreground};
    border: 1px solid {current_line};
    margin: 0px;
    padding: 0px;
}}
QTextEdit {{
    background-color: {current_line};
    color: {white};
    border: 1px solid {border};
    font-size: 16px;
    text-align: AlignCenter;
}}
QLabel {{
    color: {white};
    font-weight: bold;
}}
QLineEdit {{
    background-color: {current_line};
    color: {white};
    border: 1px solid {border};
    text-align: AlignCenter;
}}
QPushButton {{
    background-color: {current_line};
    color: {white};
    padding: 5px;
    border-radius: 5px;
    min-width: 80px;
    border: 1px solid {border};
}}
QPushButton:hover {{
    font: bold;
}}
QToolTip {{
    background-color: {green};
    color: {background};
    padding: 5px;
}}
#SnippetTextArea QToolTip {{
    background-color: {current_line};
    color: {rose};
    border: 1px solid {green};
    padding: 0px;
    margin: 0px;
}}
#typeButton {{
    background-color: {foreground};
    color: {white};
    border: 1px solid {current_line};
    padding: 5px;
    min-width: 80px;
}}
#typeButton:focus {{
    background-color: {yellow};
    font: bold;
    color: {foreground};
    border: 1px solid {border};
    padding: 5px;
    min-width: 80px;
}}
#searchButton {{
    background-color: {yellow};
    color: {background};
    border: 1px solid {border};
}}
#searchBar {{
    border: 1px solid {yellow};
    padding-left: 5px;
}}
#createButton {{
    background-color: {foreground};
    color: {rose};
    border: 1px solid {yellow};
}}
#copyButton {{
    background-color: {green};
    color: {background};
    border: 1px solid {foreground};
}}
#editButton {{
    background-color: {rose};
    color: {white};
    min-width: 20px;
}}
#editButton QToolTip {{
    background-color: {current_line};
    color: {rose};
    border: 1px solid {green};
    padding: 0px;
    margin: 0px;
}}
#editButton:hover {{
    background-color: {yellow};
}}
#deleteButton {{
    background-color: {red};
    color: {white};
    min-width: 15px;
    min-height: 5px;
}}
#deleteBox QToolTip {{
    background-color: {current_line};
    color: {rose};
    border: 1px solid {green};
    padding: 0px;
    margin: 0px;
}}
#saveButton {{
    background-color: {green};
    color: {background};
    border: 1px solid {foreground};
}}
QMenu, QComboBox {{
    background-color: {background};
    color: {white};
    text-align: center;
}}
QComboBox QAbstractItemView {{
    background-color: {background};
    color: {white};
}}
QCheckBox {{
    background-color: {background};
    color: {white};
}}
QLabel{{
    color: {white};
}}
#themePicker {{
    color: #ffffff;
    background-color: #36312c;
    border: None;
    text-align: center;
}}
"""
