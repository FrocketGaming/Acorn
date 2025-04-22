from src.data.database_manager import DatabaseManager
from src.utils.update_helper import UpdateManager
import arrow


class ConfigurationManager:
    """
    Manages the main configuration and setup process of the application.
    This includes ensuring the database is created and populated with default values.
    """

    def __init__(self) -> None:
        self.current_version = UpdateManager().get_current_version()
        self.check_configuration()

    def check_configuration(self) -> None:
        """
        Checks if the database exists, if it does not then we create it for the first time users.
        """

        db_path: str = DatabaseManager.get_db_path()
        if not db_path.exists():
            self.configure_database()
            return

        with DatabaseManager() as db:
            db.ensure_column_exists("snippets", "extension", "TEXT")
            db.ensure_column_exists("snippets", "archived", "TEXT")
            db.ensure_release_table("release", current_version=self.current_version)

    def configure_database(self) -> None:
        """
        Configures the database for first-time users to ensure the tables are create and populated with default values
        """

        with DatabaseManager() as db:
            db.create_table(
                "snippets",
                "id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, description TEXT NOT NULL, content TEXT NOT NULL, extension TEXT, archived TEXT",
            )
            db.create_table("hotkeys", "id INTEGER PRIMARY KEY, hotkey TEXT NOT NULL")
            db.create_table(
                "default_theme", "id INTEGER PRIMARY KEY, theme TEXT NOT NULL"
            )
            db.create_table("release", "release TEXT, lst_updt_ts DATE")

            db.insert_data("default_theme", ["theme"], ("Matcha",))
            db.insert_data("hotkeys", ["hotkey"], ("<alt>+<shift>+p",))
            db.insert_data(
                "release",
                ["release", "lst_updt_ts"],
                (self.current_version, arrow.now().format("YYYY-MM-DD")),
            )


if __name__ == "__main__":
    is_configured = ConfigurationManager().check_configuration()
