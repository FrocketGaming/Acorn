from pathlib import Path
import sqlite3
import polars as pl
from .query_manager import QueryManager
from src.utils.utils import UtilityManager
import logging
import arrow


class DatabaseManager:
    def establish_connection(self) -> sqlite3.Connection:
        """Establish a connection to the database and create if not exists"""
        db_path = self.get_db_path()

        try:
            # Create the database file if it doesn't exist
            if not db_path.exists():
                db_path.parent.mkdir(parents=True, exist_ok=True)
                logging.info(f"Database file created at {db_path}")

            return sqlite3.connect(db_path)
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def read_database(
        self, table_name, columns, conditions=None, group=None, order=None, params=None
    ) -> pl.DataFrame:
        """Read data from the database"""
        with self.establish_connection() as conn:
            c = conn.cursor()
            if params:
                c.execute(
                    QueryManager.create_query(
                        columns, table_name, conditions, group, order
                    ),
                    params,
                )
            else:
                c.execute(
                    QueryManager.create_query(
                        columns, table_name, conditions, group, order
                    )
                )

            # Adjust columns when using '*'
            if columns == "*":
                columns = [column[0] for column in c.description]
            else:
                columns = columns.split()

            return pl.DataFrame(c.fetchall(), schema=columns, orient="row")

    def update_database(self, table_name, columns, values, conditions=None) -> None:
        """Update data in the database"""
        with self.establish_connection() as conn:
            c = conn.cursor()

            c.execute(
                QueryManager.update_query(table_name, columns, conditions),
                values if isinstance(columns, (list, tuple)) else (values,),
            )
            conn.commit()

    def insert_data(self, table_name, columns, values) -> None:
        """Insert data into the database"""
        with self.establish_connection() as conn:
            c = conn.cursor()
            c.execute(QueryManager.insert_query(table_name, columns), values)
            conn.commit()

    def create_table(self, table_name, columns) -> None:
        """Create a new table in the database"""
        with self.establish_connection() as conn:
            c = conn.cursor()
            c.execute(QueryManager.create_table(table_name, columns))

    def delete_data(self, table_name, conditions) -> None:
        """Delete data from the database"""
        with self.establish_connection() as conn:
            c = conn.cursor()
            c.execute(QueryManager.delete_data(table_name, conditions))
            conn.commit()

    def archive_snippet_type(self, snippet_type: str) -> None:
        with self.establish_connection() as conn:
            c = conn.cursor()
            c.execute(QueryManager.archive_snippet_type(snippet_type))

    def ensure_column_exists(
        self, table_name: str, column_name: str, column_type: str
    ) -> None:
        """Ensure a specific column exists in the table, add it if missing."""
        with self.establish_connection() as conn:
            c = conn.cursor()

            c.execute(f"PRAGMA table_info({table_name})")
            existing_columns = [column[1] for column in c.fetchall()]

            if column_name not in existing_columns:
                # print(f"Adding missing column '{column_name}' to '{table_name}'")
                c.execute(
                    f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
                )
                conn.commit()
            else:
                pass
                # print(f"Column '{column_name}' already exists in '{table_name}'")

    def ensure_release_table(self, table_name: str, **kwargs) -> None:
        current_version = kwargs.get("current_version", "")

        with self.establish_connection() as conn:
            c = conn.cursor()
            try:
                c.execute(f"SELECT * FROM {table_name}")
            except sqlite3.OperationalError:
                self.create_table("release", "release TEXT, lst_updt_ts DATE")
                self.insert_data(
                    "release",
                    ["release", "lst_updt_ts"],
                    (current_version, arrow.now().format("YYYY-MM-DD")),
                )
                return

    @staticmethod
    def get_db_path() -> Path:
        db_path = Path.home() / ".acorn_vault" / "acorn.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return db_path

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connections or handle cleanup here if needed"""
        pass


if __name__ == "__main__":
    db = DatabaseManager()
    db.create_table(
        "snippets",
        "id INTEGER PRIMARY KEY, name TEXT, type TEXT, description TEXT, content TEXT",
    )
