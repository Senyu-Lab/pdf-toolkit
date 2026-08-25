from app.database.database import Database


def test_database_creates_database_file(tmp_path):
    database_path = tmp_path / "test.db"

    Database(database_path)

    assert database_path.exists()

def test_database_creates_operation_history_table(tmp_path):
    database_path = tmp_path / "test.db"

    database = Database(database_path)

    cursor = database.connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'operation_history'
        """
    )

    result = cursor.fetchone()

    assert result is not None

def test_database_returns_connection(tmp_path):
    database_path = tmp_path / "test.db"

    database = Database(database_path)

    connection = database.get_connection()

    assert connection is database.connection