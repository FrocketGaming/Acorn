from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter, QPalette
from PyQt6.QtWidgets import QApplication


class GenericSyntaxHighlighter(QSyntaxHighlighter):
    """Base class for all syntax highlighters"""

    def __init__(self, document):
        super().__init__(document)

        # Get colors from application palette
        app = QApplication.instance()
        if app:
            palette = app.palette()
            self.keyword_color = palette.color(
                QPalette.ColorRole.Base
            ).name()
            self.string_color = palette.color(QPalette.ColorRole.Link).name()
            self.comment_color = palette.color(
                QPalette.ColorRole.AlternateBase
            ).name()
            self.function_color = palette.color(QPalette.ColorRole.BrightText).name()
            self.text_color = palette.color(QPalette.ColorRole.Text).name()

        # Initialize empty rules list
        self.highlighting_rules = []

    def highlightBlock(self, text):
        """Apply highlighting to the given text block"""
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class HighlighterManager:
    def __init__(self):
        self.highlighters = {
            ".py": PythonHighlighter,
            ".sql": SQLHighlighter,
        }


class PythonHighlighter(GenericSyntaxHighlighter):
    """Python-specific syntax highlighter"""

    def __init__(self, document):
        super().__init__(document)

        # Set up highlighting rules
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(self.keyword_color))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            "and",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "exec",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "print",
            "raise",
            "return",
            "try",
            "while",
            "yield",
            "None",
            "True",
            "False",
        ]

        for word in keywords:
            pattern = QRegularExpression("\\b" + word + "\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(self.string_color))

        # Single-quoted strings
        self.highlighting_rules.append((QRegularExpression("'[^']*'"), string_format))
        # Double-quoted strings
        self.highlighting_rules.append((QRegularExpression('"[^"]*"'), string_format))

        # Functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(self.function_color))
        self.highlighting_rules.append(
            (QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"), function_format)
        )

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(self.comment_color))
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), comment_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(self.string_color))
        self.highlighting_rules.append(
            (QRegularExpression("\\b[0-9]+\\b"), number_format)
        )

        # Class names
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(self.function_color))
        class_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append(
            (QRegularExpression("\\bclass\\s+([A-Za-z0-9_]+)"), class_format)
        )


class SQLHighlighter(GenericSyntaxHighlighter):
    """SQL syntax highlighter implementation"""

    def __init__(self, document):
        super().__init__(document)

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(self.keyword_color))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        # SQL keywords
        keywords = [
            # SQL Commands
            "SELECT",
            "INSERT",
            "UPDATE",
            "DELETE",
            "CREATE",
            "ALTER",
            "DROP",
            "TRUNCATE",
            "GRANT",
            "REVOKE",
            "COMMIT",
            "ROLLBACK",
            "SAVEPOINT",
            # Clauses
            "FROM",
            "WHERE",
            "GROUP",
            "BY",
            "HAVING",
            "ORDER",
            "LIMIT",
            "OFFSET",
            "JOIN",
            "INNER",
            "OUTER",
            "LEFT",
            "RIGHT",
            "FULL",
            "CROSS",
            "UNION",
            "ALL",
            # Operators and conditionals
            "AND",
            "OR",
            "NOT",
            "IN",
            "BETWEEN",
            "LIKE",
            "IS",
            "NULL",
            "AS",
            "ON",
            "CASE",
            "WHEN",
            "THEN",
            "ELSE",
            "END",
            "EXISTS",
            "ANY",
            "SOME",
            "WITH",
            # Data types
            "INT",
            "INTEGER",
            "SMALLINT",
            "TINYINT",
            "MEDIUMINT",
            "BIGINT",
            "DECIMAL",
            "NUMERIC",
            "FLOAT",
            "DOUBLE",
            "REAL",
            "DATE",
            "DATETIME",
            "TIMESTAMP",
            "TIME",
            "YEAR",
            "CHAR",
            "VARCHAR",
            "TEXT",
            "TINYTEXT",
            "MEDIUMTEXT",
            "LONGTEXT",
            "BINARY",
            "VARBINARY",
            "BLOB",
            "TINYBLOB",
            "MEDIUMBLOB",
            "LONGBLOB",
            "ENUM",
            "SET",
            "BOOLEAN",
            "BOOL",
            # Constraints and table definitions
            "PRIMARY",
            "KEY",
            "FOREIGN",
            "REFERENCES",
            "UNIQUE",
            "CHECK",
            "DEFAULT",
            "AUTO_INCREMENT",
            "INDEX",
            "CONSTRAINT",
            # Functions
            "COUNT",
            "SUM",
            "AVG",
            "MIN",
            "MAX",
            "CURRENT_TIMESTAMP",
            "NOW",
            "CONCAT",
            "SUBSTRING",
            "TRIM",
            "LENGTH",
            "UPPER",
            "LOWER",
            "COALESCE",
            "NULLIF",
        ]

        # Add SQL keywords (case-insensitive)
        for keyword in keywords:
            pattern = QRegularExpression(
                "\\b(?i)" + keyword + "\\b"
            )  # (?i) makes it case-insensitive
            self.highlighting_rules.append((pattern, keyword_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(self.string_color))

        # String literals - single quotes
        self.highlighting_rules.append((QRegularExpression("'[^']*'"), string_format))
        # String literals - double quotes
        self.highlighting_rules.append((QRegularExpression('"[^"]*"'), string_format))

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(self.string_color))
        # Integers
        self.highlighting_rules.append(
            (QRegularExpression("\\b[0-9]+\\b"), number_format)
        )
        # Decimals
        self.highlighting_rules.append(
            (QRegularExpression("\\b[0-9]+\\.[0-9]+\\b"), number_format)
        )

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(self.comment_color))
        # Single line comments (--)
        self.highlighting_rules.append((QRegularExpression("--[^\n]*"), comment_format))
        # Multi-line comments (/* */)
        self.highlighting_rules.append(
            (QRegularExpression("/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/"), comment_format)
        )

        # Table/column identifiers format (for backticks in MySQL)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(self.function_color))
        self.highlighting_rules.append((QRegularExpression("`[^`]*`"), function_format))

        # Parentheses and brackets
        self.highlighting_rules.append(
            (QRegularExpression("[\\(\\)\\[\\]\\{\\}]"), function_format)
        )

        # Operators
        self.highlighting_rules.append((QRegularExpression("[=<>!]+"), keyword_format))
