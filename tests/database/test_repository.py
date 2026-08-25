import pytest

from app.database.database import Database
from app.database.repository import HistoryRepository


def test_add_operation(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    repository.add_operation(
        operation_type="merge",
        status="success",
        input_files=["a.pdf", "b.pdf"],
        output_files=["merged.pdf"],
    )

    operations = repository.get_operations()

    assert len(operations) == 1

    operation = operations[0]

    assert operation["operation_type"] == "merge"
    assert operation["status"] == "success"
    assert operation["input_files"] == ["a.pdf", "b.pdf"]
    assert operation["output_files"] == ["merged.pdf"]
    assert operation["error_message"] is None

def test_add_failed_operation(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    repository.add_operation(
        operation_type="merge",
        status="failed",
        input_files=["invalid.pdf"],
        output_files=[],
        error_message="Invalid PDF file.",
    )

    operations = repository.get_operations()

    operation = operations[0]

    assert operation["status"] == "failed"
    assert operation["error_message"] == "Invalid PDF file."

def test_delete_operation(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    repository.add_operation(
        operation_type="merge",
        status="success",
        input_files=["a.pdf"],
        output_files=["merged.pdf"],
    )

    operations = repository.get_operations()

    operation_id = operations[0]["id"]

    repository.delete_operation(operation_id)

    assert repository.get_operations() == []

def test_clear_operations(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    repository.add_operation(
        operation_type="merge",
        status="success",
        input_files=["a.pdf"],
        output_files=["merged.pdf"],
    )

    repository.add_operation(
        operation_type="split",
        status="success",
        input_files=["input.pdf"],
        output_files=["page1.pdf", "page2.pdf"],
    )

    assert len(repository.get_operations()) == 2

    repository.clear_operations()

    assert repository.get_operations() == []

def test_add_operation_rejects_empty_operation_type(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    with pytest.raises(ValueError):
        repository.add_operation(
            operation_type="",
            status="success",
            input_files=["a.pdf"],
            output_files=["merged.pdf"],
        )

def test_add_operation_rejects_empty_status(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    with pytest.raises(ValueError):
        repository.add_operation(
            operation_type="merge",
            status="",
            input_files=["a.pdf"],
            output_files=["merged.pdf"],
        )

def test_add_operation_rejects_invalid_input_files(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    with pytest.raises(TypeError):
        repository.add_operation(
            operation_type="merge",
            status="success",
            input_files="a.pdf",
            output_files=["merged.pdf"],
        )

def test_add_operation_rejects_invalid_output_files(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    with pytest.raises(TypeError):
        repository.add_operation(
            operation_type="merge",
            status="success",
            input_files=["a.pdf"],
            output_files="merged.pdf",
        )

def test_add_operation_rejects_invalid_error_message(tmp_path):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    with pytest.raises(TypeError):
        repository.add_operation(
            operation_type="merge",
            status="failed",
            input_files=["a.pdf"],
            output_files=[],
            error_message=123,
        )