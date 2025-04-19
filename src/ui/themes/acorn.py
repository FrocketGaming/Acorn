from src.utils.utils import UtilityManager

check_icon = UtilityManager.get_resource_path("imgs/check.png")
check_icon = str(check_icon).replace("\\", "/")

colors = {
    "background": "#3e2c22",  # Brown
    "alt_background": "#262626",
    "light_gray": "#717171",
    "foreground": "#584339",  # Light Brown
    "text": "#ffffff",
    "alt_text": "#f1ebe1",
    "main": "#584339",
    "dark_main": "#9c5c2a",
    "light_main": "#e5c8a5",
    "highlight": "#8C4A4F",  # Light Red
    "highlight_2": "#D4AF37",  # Burnt Orange
    "highlight_3": "#D4AF37",  # Gold
    "label": "#8BA888",
    "palette": {
        "Window": "light_main",
        "WindowText": "text",
        "Base": "light_main",
        "AlternateBase": "highlight_3",
        "ToolTipBase": "background",
        "ToolTipText": "foreground",
        "Text": "text",
        "Button": "foreground",
        "ButtonText": "background",
        "Highlight": "light_main",
        "HighlightedText": "foreground",
        "PlaceholderText": "light_main",
        "BrightText": "light_main",
        "Link": "light_main",
        "Light": "light_main",
        "Mid": "foreground",
        "Dark": "main",
    },
}

qss = """
	QMainWindow, QWidget {{
		background-color: {background};
	}}
	#Container {{
		background: {background};
		border: 1px solid {main};
        padding: 0px;
        margin: 0px;
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
		background-color: {foreground};
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
		border: 1px solid {main};
	}}
    QTextEdit QScrollBar:vertical {{
		background-color: {foreground};
        color: {text};
		width: 20px;
	}}
	QPushButton {{
		background-color: {foreground};
		color: {background};
		border: none;
		padding: 5px;
		min-width: 80px;
	}}
	QLabel {{
		color: {alt_text};
		font-weight: bold;
	}}
	QLineEdit {{
		background-color: {background};
		color: {text};
		border: 1px solid {main};
		text-align: AlignCenter;
		margin-right: 4px;
	}}
    
    /* ========== Custom Title Bar CSS ========== */
	#titleBarLayout #iconLabel {{
		background-color: {main};
		color: {text};
		padding-left: 10px;
	}}
	#titleBarLayout QWidget {{
		background-color: {main};
		color: {text};
		margin: 0px;
		padding: 0px;
		font-weight: bold;
	}}
	#titleBarLayout #closeButton {{
		background-color: {main};
        color: {text};
		margin: 0px;
		border: none;
	}}
	#titleBarLayout #closeButton:hover {{
		background-color: {foreground};
        color: {light_main};
		border: none;
	}}

	/* ========== Snippet Display Area CSS ========== */
	#SnippetTextArea {{
		border: 1px solid {light_gray};
		font-size: 14px;
		font-weight: normal;
		min-height: 28px;
		max-height: 28px;
		min-width: 670px;
		max-width: 695px;
    padding: 0px;
    margin: 0px;
	}}
	#SnippetTextArea QTextarea {{
		padding: 0px;
		margin: 0px;
	}}
	#contentScrollArea {{
		background-color: {foreground};
		border-top: 1px solid {light_main};
		border-bottom: 1px solid {light_main};
		padding: 0px;
        min-width: 30px;
	}}
	#contentWidget {{
		background-color: {foreground};
		padding: 0px;
		margin: 0px;
	}}
    QToolTip {{
		background-color: {background};
		color: {text};
		border: 1px solid {main};
		padding: 5px;
	}}

	/* ========== Snippet Type Button CSS ========== */
    #typeScrollArea {{
		border: none;
    }}
    #typeWidget {{
		margin: 0px;
		padding: 0px;
	}}
	#typeButton {{
		background-color: {foreground};
		color: {text};
		font: bold;
		border: 1px solid {foreground};
		padding: 4px;
		min-width: 80px;
	}}
	#typeButton:hover {{
		font: bold;
		background-color: {light_main};
		color: {background};
	}}
	#typeButton:focus {{
		background-color: {main};
		color: {background};
		font: bold;
		border: none;
		padding: 4px;
		min-width: 80px;
	}}
    #typeButton:focus:hover {{
		background-color: {light_main};
    }}
	#typeButtonArchived {{
		background-color: {foreground};
		color: {text};
		font: bold;
		border: 1px solid {highlight_3};
		padding: 4px;
		min-width: 80px;
	}}
	#typeButtonArchived:hover {{
		font: bold;
		background-color: {alt_text};
		color: {background};
	}}
	#typeButtonArchived:focus {{
		background-color: {main};
		color: {background};
		font: bold;
		border: none;
		padding: 4px;
		min-width: 80px;
	}}

	/* ========== Search Bar CSS ========== */
	#searchBar {{
		border: 1px solid {light_main};
		color: {text};
		padding-left: 5px;
		margin-left: 4px;
        placeholder-text-color: {light_main};
	}}
	#searchButton {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {foreground};
		border-radius: 10px;
	}}
	#searchButton:hover {{
		background-color: {main};
		color: {text};
	}}
	#clearButton {{
		background-color: {background};
		color: {text};
		margin: 0px 4px 0px 0px;
		border-radius: 10px;
	}}
	#clearButton:hover {{
		background-color: {highlight_3};
		color: {background};
	}}

	/* ========== Create Snippet Button CSS ========== */
	#createButton {{
		background-color: {highlight_3};
		color: {background};
		font-weight: bold;
		margin: 0px 4px 4px 4px;
	}}
	#createButton:hover {{
		background-color: {foreground};
		color: {text};
		font: bold;
	}}

	/* ========== Delete, Copy, Edit Snippet CSS ========== */
	#copyButton {{
		background-color: {light_main};
		border: 1px solid {foreground};
		min-width: 15px;
		max-width: 15px;
		min-height: 10px;
		border-radius: 10px;
	}}
	#copyButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {light_main};
		padding: 0px;
		margin: 0px;
	}}
	#copyButton:hover {{
		background-color: {alt_text};
	}}
	#editButton {{
		background-color: {light_main};
		border: 1px solid {foreground};
		min-width: 15px;
		max-width: 15px;
		min-height: 10px;
		border-radius: 8px;
	}}
	#editButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {main};
		padding: 0px;
		margin: 0px;
	}}
	#editButton:hover {{
		background-color: {alt_text};
	}}
	#deleteButton {{
		background-color: {highlight};
        border: none;
		color: {text};
		min-width: 10px;
		max-width: 10px;
		max-height: 10px;
		border-radius: 5px;
	}}
	#deleteButton QToolTip {{
		background-color: {foreground};
		color: {text};
		border: 1px solid {main};
		padding: 0px;
		margin: 0px;
	}}
	#deleteButton:hover {{
		color: {foreground};
		font: bold;
	}}

	/* ========== Confirmation Popup CSS ========== */
	#deleteConfirmationLabel {{
		qproperty-alignment: AlignCenter;
		margin-bottom: 4px;
		margin-right: 4px;
		margin-left: 4px;
		color: {text};
	}}
	#deleteConfirmationButton {{
		max-width: 50px;
		margin-bottom: 4px;
		margin-right: 4px;
		margin-left: 4px;
		color: {background};
		background-color: {highlight_3};
	}}
	#deleteConfirmationButton:hover {{
		color: {text};
		background-color: {highlight_2};
	}}
	#deleteConfirmationCloseButton {{
		margin-bottom: 4px;
		margin-right: 4px;
		color: {text};
	}}
	#deleteConfirmationCloseButton:hover {{
		color: {text};
		background-color: {main};
	}}
		
	/* ========== Snippet Popup CSS ========== */
	#snippetTextArea {{
		border-top: 1px solid {light_main};
		border-bottom: 1px solid {light_main};
		border-left: 1px solid {main};
		border-right: 1px solid {main};
        background-color: {background};

	}}
	#Popup {{
		border: 1px solid {main};
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
	#saveButton {{
		margin-bottom: 4px;
		margin-left: 4px;
		background-color: {main};
        color: {text};
        border: 1px solid {light_main};
	}}
	#saveButton:hover {{
		background-color: {background};
        color: {text};
	}}
	#closeButton {{
		margin-bottom: 4px;
		margin-right: 4px;
		background-color: {foreground};
		border: 1px solid {foreground};
		color: {text};
	}}
	#closeButton:hover {{
		color: {background};
		background-color: {highlight_2};
	}}

	/* ========== Archive & Release Notes Section CSS ========== */
	#archiveCheckbox {{
		color: {text};
		margin-left: 4px;
        font-size: 14px;   
  }}
	#archiveCheckbox::indicator {{
		background-color: {background};
		border: 1px solid {text};
        width: 12px;
		height: 12px;
		border-radius: 3px;
	}}
	#archiveCheckbox::indicator:checked {{
		background-color: {main};
		border: 1px solid {text};
		image: url({icon});
		border-radius: 3px;
	}}
	#releaseNotesButton {{
		color: {text};
		font-size: 18px;
		font-weight: bold;
		background-color: {background};
		margin-right: 4px;
		min-width: 14px;
		padding: 0px;
	}}
	#releaseNotesButton:hover {{
		color: {main};
		font-size: 18px;
		font-weight: bold;
		background-color: {background};
	}}

 	/* ========== System Tray CSS ========== */
	#hotkeyLayout {{
		border: 1px solid {main};
		}}
	#keyLayout {{
		margin-left: 4px;
		}}
	#keyCombo {{
		margin-right: 4px;
	}}
		#okButton {{
		background-color: {main};
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
		background-color: {highlight_2};
		color: {background};
	}}
	#checkBox {{
		color: {text};
				margin-left: 4px;
				margin-right: 4px;
		}}
	#checkBox::indicator:checked {{
		background-color: {main};
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
		background-color: {highlight_3};
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
		border: 1px solid {main};
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
				border: 1px solid {main};
				color: {text}
	}}
    
 	/* ========== Context Menu CSS ========== */
	#contextMenu {{
		background-color: {background};
		border: 1px solid {highlight_3};
		color: {text};
	}}

	/* ========== Generic Popup CSS ========== */
	#popupContent {{
		padding: 10px;
		margin: 10px;
		border: 1px solid {dark_main};
		font-size: 14px;
	}}
	#popupCloseButton {{
		color: {text};
		background-color: {foreground};
		margin: 4px;
		border: none;
	}}
	#popupCloseButton:hover {{
		background-color: {highlight_2};
	}}
	"""
qss = qss.replace("{icon}", check_icon)
