from src.utils.utils import UtilityManager

check_icon = UtilityManager.get_resource_path("imgs/check.png")
check_icon = str(check_icon).replace("\\", "/")

colors = {
    "background": "#2E2F2F",
    "alt_background": "#262626",
    "foreground": "#3b3b3b",
    "text": "#ffffff",
    "alt_text": "#f1ebe1",
    "green": "#8BA888",
    "dark_green": "#6d896a",
    "green_border": "#435740",
    "highlight": "#cddacc",
    "orange": "#ffb86f",
    "red": "#c83e4d",
    "label": "#8BA888",
    "palette": {
        "Window": "background",
        "WindowText": "foreground",
        "Base": "background",
        "AlternateBase": "foreground",
        "ToolTipBase": "background",
        "ToolTipText": "foreground",
        "Text": "text",
        "Button": "foreground",
        "ButtonText": "background",
        "Highlight": "label",
        "HighlightedText": "background",
    },
}

qss = """
	QMainWindow, QWidget {{
		background-color: {green};
	}}
		#Container {{
		background: {green};
		border: 1px solid {background};
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
		color: {text};
		text-align: center; 
		max-width: 150px;
	}}
	QMenu::item:selected {{
		background-color: {dark_green};
		color: {text};
	}}
	QVBoxLayout {{
		padding: 0px;
		margin: 0px;
	}}
	QScrollArea QPushButton {{
		background-color: {background};
		color: {foreground};
		border-radius: 10px;
		border: 1px solid {green};
	}}
	QPushButton {{
		background-color: {foreground};
		color: {background};
		border: none;
		padding: 5px;
		min-width: 80px;
	}}
	QPushButton:hover {{
		background-color: {red};
	}}
	QToolTip {{
		background-color: {background};
		color: {text};
		border: 1px solid {foreground};
		padding: 5px;
	}}
	QLabel {{
		color: {alt_text};
		font-weight: bold;
	}}
	QLineEdit {{
		background-color: {background};
		color: {text};
		border: 1px solid {green};
		text-align: AlignCenter;
		margin-right: 4px;
	}}
	#titleBarLayout #iconLabel {{
		background-color: {green};
		color: {text};
		padding-left: 10px;
	}}
	#titleBarLayout QWidget {{
		background-color: {green};
		color: {text};
		margin: 0px;
		padding: 0px;
		font-weight: bold;
	}}
	#titleBarLayout #closeButton {{
		background-color: {green};
		margin: 0px;
		border: none;
	}}
	#titleBarLayout #closeButton:hover {{
		background-color: {alt_text};
		border: none;
	}}
	#typeWidget {{
		margin: 0px;
		padding: 0px;
	}}
	#SnippetTextArea {{
		border: 1px solid {green_border};
		max-height: 34px;
	}}
	#SnippetTextArea QTextarea {{
		padding: 0px;
		margin: 0px;
	}}
	#contentScrollArea {{
		background-color: {foreground};
		border: 1px solid {green_border};
		padding: 0px;
		margin: 0px 4px 0px 4px;
	}}
	#contentWidget {{
		background-color: {foreground};
		padding: 0px;
		margin: 0px;
	}}
	#typeButton {{
		background-color: {foreground};
		color: {text};
		font: bold;
		border: 1px solid {foreground};
		padding: 5px;
		min-width: 80px;
	}}
	#typeButton:hover {{
		font: bold;
		background-color: {alt_text};
		color: {background};
	}}
	#typeButton:focus {{
		background-color: {green};
		color: {background};
		font: bold;
		border: none;
		padding: 5px;
		min-width: 80px;
	}}
	#searchBar {{
		border: 1px solid {highlight};
		color: {text};
		padding-left: 5px;
		margin-left: 4px;
	}}
	#searchButton {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {foreground};
		border-radius: 10px;
	}}
	#searchButton:hover {{
		background-color: {green};
		color: {background};
	}}
	#clearButton {{
		background-color: {background};
		color: {text};
		margin: 0px 4px 0px 0px;
		border-radius: 10px;
	}}
	#clearButton:hover {{
		background-color: {orange};
		color: {background};
	}}
	#createButton {{
		background-color: {orange};
		color: {background};
				font-weight: bold;
		margin: 0px 4px 4px 4px;
	}}
	#createButton:hover {{
		background-color: {foreground};
		color: {text};
		font: bold;
	}}
	#copyButton {{
		background-color: {green};
		border: 1px solid {foreground};
				min-width: 8px;
				min-height: 10px;
				border-radius: 10px;
	}}
	#copyButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {green};
		padding: 0px;
		margin: 0px;
	}}
	#copyButton:hover {{
				background-color: {alt_text};
	}}
	#editButton {{
		background-color: {text};
		border: 1px solid {foreground};
				min-width: 15px;
		min-height: 10px;
		border-radius: 8px;
	}}
	#editButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {green};
		padding: 0px;
		margin: 0px;
	}}
	#editButton:hover {{
		background-color: {alt_text};
	}}
	#deleteButton {{
		background-color: {red};
		color: {text};
		border: 1px solid {foreground};
		min-width: 5px;
		max-height: 10px;
		border-radius: 5px;
	}}
	#deleteButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {green};
		padding: 0px;
		margin: 0px;
	}}
	#deleteButton:hover {{
		color: {foreground};
		font: bold;
	}}
	#saveButton {{
		margin-bottom: 4px;
		margin-left: 4px;
		background-color: {green};
	}}
	#closePopupButton {{
		margin-bottom: 4px;
		margin-right: 4px;
		color: {text};
	}}
	#deleteConfirmationButton {{
		margin-bottom: 4px;
		margin-right: 4px;
		color: {text};
	}}
		
	/* ========== Snippet Popup CSS ========== */
	#snippetTextArea {{
		border: 1px solid {green_border};
		margin-left: .2em;
		margin-right: .2em;
	}}
		#Popup {{
		border: 1px solid {green};
	}}
	#InputField {{
		min-width: 450px;	
		max-width: 580px;
	}}
	#TypeInputField {{
		max-width: 510px;
	}}
	#typeLabel {{
		margin-left: .3em;
		margin-right: .3em;
	}}
	#PopupLabel {{
		margin-left: .3em;
		margin-right: .3em;
	}}
		/* System Tray CSS */
	#hotkeyLayout {{
		border: 1px solid {green};
		}}
	#keyLayout {{
		margin-left: 4px;
		}}
	#keyCombo {{
		margin-right: 4px;
	}}
		#okButton {{
		background-color: {green};
				margin-left: 4px;
				margin-bottom: 4px;
		}}
	#okButton:hover {{
		background-color: {highlight};
	}}
	#cancelButton {{
		background-color: {alt_background};
				color: {text};
				margin-right: 4px;
		margin-bottom: 4px;
	}}
	#cancelButton:hover {{
		background-color: {red};
		color: {background};
	}}
	#checkBox {{
		color: {text};
				margin-left: 4px;
				margin-right: 4px;
		}}
	#checkBox::indicator:checked {{
		background-color: {green};
				border: 1px solid {text};
				image: url({icon});
				color: {background};
	}}
	#checkBox::indicator:unchecked {{
		background-color: {background};
				border: 1px solid {text};
				color: {background};
	}}

	/* ========== Update Button & Text ========== */
	#themeLayout {{
		padding-top: 0px;
		}}
		#themePicker {{
		color: {text};
		background-color: {foreground};
		border: None;
		text-align: center;
	}}
	#updateButton {{
		background-color: {orange};
		min-width: 10px;
		border-radius: 4px;
		font-weight: bold;
				font-size: 14px;
				padding: 3px;
				min-height: 9px;
		color: {background};
	}}
	#updateLabel {{
		margin-left: 10px;
		padding-left 10px;
		color: {text};
	}}

	/* ========== File Extension CSS ========== */
	QComboBox {{
		background-color: {foreground};
		border: 1px solid {green};
		color: {text};
		text-align: center;
		padding-left: 3px;
	}}
	QComboBox QAbstractItemView {{
		border: none;
		outline: none;
	}}
	QComboBox QAbstractItemView::item {{
		border: none; 
		padding: 4px; 
				color: {text};
	}}
	QComboBox QAbstractItemView::item:hover {{
		background-color: {background};
				border: 1px solid {green};
				color: {text}
	}}
	"""
qss = qss.replace("{icon}", check_icon)
