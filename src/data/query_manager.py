from typing import List


class QueryManager:
    """
    Class to manage queries to the database.
    """

    @staticmethod
    def create_table(table_name: str, table_columns: str) -> str:
        """
        Generic method to create a table in the database.

        Args:
            table_name (str): The name of the table to create
            table_columns (str): The columns of the table to create

        Returns:
            str: The SQL query to create the table
        """

        return f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_columns}
        )
        """

    @staticmethod
    def update_query(table_name: str, columns: str, conditions=None) -> str:
        """
        Query to update data in the database
        """

        if isinstance(columns, str):
            set_clause = f"{columns} = ?"
        elif isinstance(columns, (list, tuple)):
            set_clause = ", ".join([f"{col} = ?" for col in columns])

        query = f"UPDATE {table_name} SET {set_clause}"

        if conditions:
            query += f" WHERE {conditions}"
        return query

    @staticmethod
    def insert_query(table_name: str, columns: List[str]) -> str:
        """Query to insert data into the database"""

        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))

        return f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})"""

    @staticmethod
    def create_query(
        columns: list | str,
        table_name: str,
        conditions: str = None,
        group: str = None,
        order: str = None,
    ) -> str:
        """
        Generates a SELECT query for the database.

        Args:
            columns (list | str): The column(s) to retrieve.
            table_name (str): The table to retrieve data from.
            conditions (str, optional): The WHERE clause conditions.

        Returns:
            str: The SQL SELECT query.
        """

        if isinstance(columns, str):
            if columns != "*":
                columns = [columns]
        elif isinstance(columns, (list, tuple)):
            columns = [col for col in columns]

        query = f"SELECT {', '.join(columns)} FROM {table_name}"

        if conditions:
            query += f" WHERE {conditions}"
        if group:
            query += f" GROUP BY {group}"
        if order:
            query += f" ORDER BY {order}"

        return query

    @staticmethod
    def snippet_table_query() -> str:
        """Query to create the snippets table in the database"""

        return QueryManager.create_table(
            "snippets",
            """
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            content TEXT NOT NULL
            """,
        )

    @staticmethod
    def hotkey_table_query() -> str:
        """Query to create the hotkeys table in the database"""

        return QueryManager.create_table(
            "hotkeys",
            """
            id INTEGER PRIMARY KEY,
            hotkey TEXT NOT NULL
            """,
        )

    @staticmethod
    def archive_snippet_type(snippet_type: str) -> str:
        """Query to archive snippets of a specific type"""
        return f"""
        UPDATE snippets
        SET archived = 'Y'
        WHERE type = '{snippet_type}'
        AND archived IS NULL
        OR archived = 'N'
        """

    @staticmethod
    def delete_data(table_name, conditions) -> str:
        """Query to delete data from the database"""

        return f"DELETE FROM {table_name} WHERE {conditions}"
