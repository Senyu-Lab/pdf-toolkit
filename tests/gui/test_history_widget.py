from app.database.database import Database
from app.database.repository import HistoryRepository
from gui.history_widget import HistoryWidget
from gui.i18n import LanguageManager


def test_history_widget_initializes_without_repository(qtbot):
    widget = HistoryWidget()

    qtbot.addWidget(widget)

    assert widget.history_table.rowCount() == 0


def test_history_widget_displays_operations(
    qtbot,
    tmp_path,
):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    repository.add_operation(
        operation_type="merge",
        status="success",
        input_files=[
            "a.pdf",
            "b.pdf",
        ],
        output_files=[
            "merged.pdf",
        ],
    )

    widget = HistoryWidget(
        history_repository=repository,
    )

    qtbot.addWidget(widget)

    assert widget.history_table.rowCount() == 1

    assert (
        widget.history_table.item(0, 1).text()
        == "merge"
    )

    assert (
        widget.history_table.item(0, 2).text()
        == "success"
    )

    assert (
        widget.history_table.item(0, 3).text()
        == "a.pdf, b.pdf"
    )

    assert (
        widget.history_table.item(0, 4).text()
        == "merged.pdf"
    )


def test_history_widget_refreshes_history(
    qtbot,
    tmp_path,
):
    database = Database(tmp_path / "test.db")
    repository = HistoryRepository(database)

    widget = HistoryWidget(
        history_repository=repository,
    )

    qtbot.addWidget(widget)

    assert widget.history_table.rowCount() == 0

    repository.add_operation(
        operation_type="split",
        status="success",
        input_files=[
            "input.pdf",
        ],
        output_files=[
            "input_1.pdf",
            "input_2.pdf",
        ],
    )

    widget.refresh_history()

    assert widget.history_table.rowCount() == 1


def test_history_widget_refreshes_with_language(
    qtbot,
):
    language = LanguageManager("en")

    widget = HistoryWidget(
        language_manager=language,
    )

    qtbot.addWidget(widget)

    assert widget.title_label.text() == "History"

    language.set_language("zh")

    widget.refresh_ui()

    assert widget.title_label.text() == "操作历史"
    assert widget.refresh_button.text() == "刷新"