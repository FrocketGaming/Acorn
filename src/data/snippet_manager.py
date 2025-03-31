from typing import List
from .database_manager import DatabaseManager
from pathlib import Path
import polars as pl
from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)


class SnippetManager(QObject):
    """Manages the snippets and operations involved with snippets such as Search, Delete, Edit, etc."""

    snippet_updated = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        # self.file_watcher = QFileSystemWatcher()
        # self.file_watcher.fileChanged.connect(self._on_file_changed)
        # self.temp_files = {}  # {snippet_id: (file_path, process_id)}
        # self.vscode_path = self._find_vscode()
        self.db = DatabaseManager()
        self.db_release = self.db.read_database("release", "release")
        self.extension_map = {
            "": "",
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "html": ".html",
            "css": ".css",
            "sql": ".sql",
            "json": ".json",
            "markdown": ".md",
            "yaml": ".yml",
            "dockerfile": ".dockerfile",
            "shell": ".sh",
            "powershell": ".ps1",
            "rust": ".rs",
            "go": ".go",
            "cpp": ".cpp",
            "c": ".c",
            "java": ".java",
            "php": ".php",
            "ruby": ".rb",
        }

    def archive_snippet_type(self, snippet_type: str) -> None:
        self.db.archive_snippet_type(snippet_type)

    def perform_search(self, query: str, archived_status: bool = False) -> List:
        """
        Performs the search operation on the snippets based on the query provided.

        Args:
            query (str): The search query.

        Returns:
            List: A list of snippets that match the search query. If the query is empty, returns all snippets.
        """

        if not query:  # Blank search essentially
            return [snippet for snippet in self.get_snippets(archived=archived_status)]
        if "*" in query:  # Wildcard search
            query = query.replace("*", "", 1)
            return [
                snippet
                for snippet in self.get_snippets(archived=archived_status)
                if query.lower() in snippet["description"].lower()
                or query.lower() in snippet["name"].lower()
                or query.lower() in snippet["content"].lower()
            ]

        # All normal search results
        return [
            snippet
            for snippet in self.get_snippets(archived=archived_status)
            if query.lower() in snippet["description"].lower()
            or query.lower() in snippet["name"].lower()
        ]

    def get_snippet_types(self, archived: bool = False) -> List:
        """
        Gets the unique snippet types from the database.

        Returns:
            List: A sorted list of unique snippet types.
        """

        if archived:
            snippet_types: pl.DataFrame = self.db.read_database(
                table_name="snippets",
                columns="type",
                group="type",
                conditions="archived = 'Y'",
            )
            results = sorted(snippet_types["type"], key=str.casefold)
        else:
            snippet_types: pl.DataFrame = self.db.read_database(
                table_name="snippets",
                columns="type",
                group="type",
                conditions="(archived = 'N' OR archived IS NULL)",
            )
            results = sorted(snippet_types["type"], key=str.casefold)

        return results

    def check_archive_status(self, snippet_type: str) -> bool:
        if snippet_type:
            archived_status: pl.DataFrame = self.db.read_database(
                "snippets", "archived", "type = ?", params=(snippet_type[0],)
            )
            if archived_status.is_empty() or archived_status["archived"][0] == "N":
                return True
            return False
        return True

    def get_snippets(
        self, snippet_type: str = None, columns: str = "*", archived: bool = False
    ) -> List:
        """
        Pulls all snippets from the database based on the snippet type. If not type is passed then returns all snippets.

        Args:
            snippet_type (str): The snippet type to filter by.

        Returns:
            List: A list of dictionaries containing the snippets.
        """

        if snippet_type and not archived:
            results = self.db.read_database(
                "snippets",
                f"{columns}",
                conditions="type = ? AND (archived = 'N' OR archived IS NULL)",
                params=(snippet_type,),
            ).to_dicts()
        elif snippet_type and archived:
            results = self.db.read_database(
                "snippets",
                f"{columns}",
                conditions="type = ? AND archived = 'Y'",
                params=(snippet_type,),
            ).to_dicts()
        elif not snippet_type and archived:
            results = self.db.read_database(
                "snippets",
                f"{columns}",
                conditions="archived = 'Y'",
            ).to_dicts()
        else:
            results = self.db.read_database(
                "snippets",
                f"{columns}",
                conditions="(archived = 'N' OR archived IS NULL)",
            ).to_dicts()

        return results

    def save_snippet(self, new_snippet: dict) -> None:
        """
        Saves the created snippet to the database.
        values contain: name, type, description, content, file extension

        Args:
            new_snippet (dict): A dictionary containing the snippet details.

        Returns:
            None
        """

        columns: list[str] = list(new_snippet.keys())
        values: tuple[str] = tuple(new_snippet.values())

        self.db.insert_data("snippets", columns, values)

    def update_existing_snippet(
        self, new_snippet: dict, existing_snippet: dict
    ) -> None:
        """
        Updates an existing snippet in the database.

        Args:
            new_snippet (dict): A dictionary containing the updated snippet details.
            existing_snippet (dict): A dictionary containing the existing snippet details.

        Returns:
            None
        """

        columns: list[str] = [key for key in new_snippet.keys() if key != "id"]
        values: tuple[str] = tuple(new_snippet[key] for key in columns)
        condition: str = f"id = {existing_snippet['id']}"

        self.db.update_database("snippets", columns, values, condition)

    def delete_snippet(self, snippet_id: int) -> None:
        """
        Deletes a snippet from the database using the snippet id.

        Args:
            snippet_id (int): The id of the snippet to delete.

        Returns:
            None
        """

        self.db.delete_data("snippets", f"id = {snippet_id}")

    # =========== VS CODE INTEGRATION BELOW ===========
    # TODO:

    # def _find_vscode(self) -> Path:
    # system = platform.system()

    # if system == "Windows":
    #     paths = [
    #         Path("C:/Program Files/Microsoft VS Code/Code.exe"),
    #         Path("C:/Program Files (x86)/Microsoft VS Code/Code.exe"),
    #         Path.home() / "AppData/Local/Programs/Microsoft VS Code/Code.exe",
    #         Path.home() / "AppData/Local/Programs/Microsoft VS Code/bin/code",
    #     ]
    # elif system == "Darwin":  # macOS
    #     paths = [
    #         Path(
    #             "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
    #         ),
    #         Path("/usr/local/bin/code"),
    #     ]
    # else:  # Linux
    #     paths = [
    #         Path("/usr/bin/code"),
    #         Path("/usr/local/bin/code"),
    #         Path.home() / ".local/bin/code",
    #     ]

    # for path in paths:
    #     if path.exists():
    #         return path
    # return None

    # TODO:
    # # def edit_in_vscode(self, snippet_id: int) -> None:
    # snippet = (
    #     self.db
    #     .read_database("snippets", "*", "id = ?", (snippet_id,))
    #     .to_dicts()[0]
    # )
    # print(snippet)

    # temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".sql", delete=False)
    # temp_file.write(snippet["content"])
    # temp_file.close()

    # if not self.vscode_path:
    #     raise Exception(
    #         "VSCode not found. Please install VSCode or add it to PATH."
    #     )

    # process = subprocess.Popen([self.vscode_path, temp_file.name])
    # self.temp_files[snippet_id] = (temp_file.name, process.pid)
    # self.file_watcher.addPath(temp_file.name)
    # # TODO:
    # # def _on_file_changed(self, path):
    # snippet_id = None
    # for sid, (fpath, pid) in self.temp_files.items():
    #     if fpath == path:
    #         snippet_id = sid
    #         if not psutil.pid_exists(pid):
    #             break
    #         return  # VSCode still running

    # if snippet_id is None:
    #     return

    # with open(path, "r") as f:
    #     new_content = f.read()

    # self.update_existing_snippet(
    #     {"content": new_content, "id": snippet_id}, {"id": snippet_id}
    # )

    # self.file_watcher.removePath(path)
    # Path(path).unlink()
    # del self.temp_files[snippet_id]

    # self.snippet_updated.emit(snippet_id, new_content)

    # # TODO:
    # # def cleanup(self):
    # for _, (path, _) in self.temp_files.items():
    #     try:
    #         Path(path).unlink()
    #     except Exception:
    #         pass
    # self.temp_files.clear()
