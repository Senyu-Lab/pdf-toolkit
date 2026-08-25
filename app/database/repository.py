import json
from datetime import datetime
from pathlib import Path

from app.database.database import Database

SQL_DIRECTORY = Path(__file__).parent / "sql"


class HistoryRepository:
    def __init__(self, database: Database):
        self.database = database

    # Load an SQL statement from the SQL directory.
    def _load_sql(self, filename: str) -> str:
        sql_file = SQL_DIRECTORY / filename

        with sql_file.open("r", encoding="utf-8") as file:
            return file.read()

    def add_operation(
        self,
        operation_type: str,
        status: str,
        input_files: list[str],
        output_files: list[str],
        error_message: str | None = None,
    ):
        self._validate_operation(
            operation_type,
            status,
            input_files,
            output_files,
            error_message,
        )

        sql = self._load_sql("insert_history.sql")

        created_at = datetime.now().astimezone().isoformat()

        self.database.get_connection().execute(
            sql,
            (
                operation_type,
                status,
                created_at,
                json.dumps(input_files),
                json.dumps(output_files),
                error_message,
            ),
        )

        self.database.get_connection().commit()

    def get_operations(self) -> list[dict]:
        sql = self._load_sql("select_history.sql")

        cursor = self.database.get_connection().execute(sql)

        operations = []

        for row in cursor.fetchall():
            operations.append(
                {
                    "id": row[0],
                    "operation_type": row[1],
                    "status": row[2],
                    "created_at": row[3],
                    "input_files": json.loads(row[4]),
                    "output_files": json.loads(row[5]),
                    "error_message": row[6],
                }
            )

        return operations

    def delete_operation(self, operation_id: int):
        sql = self._load_sql("delete_history.sql")

        self.database.get_connection().execute(
            sql,
            (operation_id,),
        )

        self.database.get_connection().commit()

    def clear_operations(self):
        sql = self._load_sql("clear_history.sql")

        self.database.get_connection().execute(sql)
        self.database.get_connection().commit()

    def _validate_operation(
            self,
            operation_type: str,
            status: str,
            input_files: list[str],
            output_files: list[str],
            error_message: str | None,
    ):
        if not operation_type:
            raise ValueError("Operation type cannot be empty.")

        if not status:
            raise ValueError("Status cannot be empty.")

        if not isinstance(input_files, list):
            raise TypeError("Input files must be a list.")

        if not isinstance(output_files, list):
            raise TypeError("Output files must be a list.")

        if error_message is not None and not isinstance(error_message, str):
            raise TypeError("Error message must be a string or None.")