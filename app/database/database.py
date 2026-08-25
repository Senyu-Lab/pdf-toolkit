import sqlite3
from pathlib import Path

from PySide6.QtCore import QStandardPaths


class Database:
    def __init__(self, database_path: Path | None = None):
        self.database_path = (
            database_path
            if database_path is not None
            else self._get_default_database_path()
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.database_path,
        )

        self._initialize_database()

    def _get_default_database_path(self) -> Path:
        data_location = QStandardPaths.writableLocation(
            QStandardPaths.AppDataLocation,
        )

        return Path(data_location) / "history.db"

    def _initialize_database(self):
        schema = Path(__file__).parent / "sql" / "schema.sql"

        with schema.open("r", encoding="utf-8") as file:
            self.connection.executescript(file.read())

        self.connection.commit()

    def get_connection(self) -> sqlite3.Connection:
        return self.connection