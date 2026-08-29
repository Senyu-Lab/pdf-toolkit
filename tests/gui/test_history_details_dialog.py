from gui.history_details_dialog import HistoryDetailsDialog
from gui.i18n import LanguageManager

language = LanguageManager("en")



def test_history_details_dialog_displays_operation(qtbot):
    operation = {
        "id": 1,
        "operation_type": "merge",
        "status": "success",
        "created_at": "2026-08-29T12:00:00+09:00",
        "input_files": [
            "a.pdf",
            "b.pdf",
        ],
        "output_files": [
            "merged.pdf",
        ],
        "error_message": None,
    }

    dialog = HistoryDetailsDialog(
        language,
        operation,
    )

    qtbot.addWidget(dialog)

    assert dialog.operation_label.text() == "merge"
    assert dialog.status_label.text() == "success"

    assert (
        dialog.input_files_list.count()
        == 2
    )

    assert (
        dialog.output_files_list.count()
        == 1
    )

    assert dialog.error_label.text() == "-"

def test_history_details_dialog_displays_error(
    qtbot,
):
    operation = {
        "id": 2,
        "operation_type": "split",
        "status": "failed",
        "created_at": "2026-08-29T12:00:00+09:00",
        "input_files": [
            "invalid.pdf",
        ],
        "output_files": [],
        "error_message": "Invalid PDF file.",
    }

    dialog = HistoryDetailsDialog(
        language,
        operation,
    )

    qtbot.addWidget(dialog)

    assert dialog.status_label.text() == "failed"

    assert (
        dialog.error_label.text()
        == "Invalid PDF file."
    )