from pathlib import Path

import pymupdf
from PySide6.QtWidgets import QMessageBox

from gui.delete_widget import DeleteWidget


def create_test_pdf(path: Path, page_count: int = 5):
    doc = pymupdf.open()

    for _ in range(page_count):
        doc.new_page()

    doc.save(path)
    doc.close()


def test_parse_page_ranges():
    result = DeleteWidget.parse_page_ranges("2,4-6")

    assert result == [(2, 2), (4, 6)]


def test_parse_page_ranges_with_spaces():
    result = DeleteWidget.parse_page_ranges(" 1 , 3 - 5 ")

    assert result == [(1, 1), (3, 5)]


def test_parse_page_ranges_invalid():
    try:
        DeleteWidget.parse_page_ranges("")
    except ValueError as exc:
        assert str(exc) == "No valid page ranges were entered."
    else:
        raise AssertionError("ValueError was not raised")


def test_choose_pdf(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    pdf = tmp_path / "input.pdf"
    create_test_pdf(pdf)

    monkeypatch.setattr(
        "gui.delete_widget.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (str(pdf), "PDF Files (*.pdf)"),
    )

    widget.choose_pdf()

    assert widget.input_file == pdf
    assert widget.input_label.text() == f"PDF: {pdf.name}"


def test_choose_output(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    output = tmp_path / "modified.pdf"

    monkeypatch.setattr(
        "gui.delete_widget.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: (
            str(output),
            "PDF Files (*.pdf)",
        ),
    )

    widget.choose_output()

    assert widget.output_file == output
    assert widget.output_label.text() == f"Output: {output}"


def test_delete_file_success(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "modified.pdf"

    create_test_pdf(input_file, 5)

    widget.input_file = input_file
    widget.output_file = output_file
    widget.range_input.setText("2")

    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args, **kwargs: None,
    )

    widget.delete_file()

    assert output_file.exists()

    doc = pymupdf.open(output_file)
    assert len(doc) == 4
    doc.close()


def test_delete_file_without_input(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    widget.output_file = tmp_path / "modified.pdf"
    widget.range_input.setText("2")

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args),
    )

    widget.delete_file()

    assert len(messages) == 1
    assert messages[0][1] == "PDF not selected"


def test_delete_file_without_pages(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    create_test_pdf(input_file)

    widget.input_file = input_file
    widget.output_file = tmp_path / "modified.pdf"

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args),
    )

    widget.delete_file()

    assert len(messages) == 1
    assert messages[0][1] == "Pages not entered"


def test_delete_file_without_output(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    create_test_pdf(input_file)

    widget.input_file = input_file
    widget.range_input.setText("2")

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args),
    )

    widget.delete_file()

    assert len(messages) == 1
    assert messages[0][1] == "Output not selected"


def test_delete_file_invalid_range(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    create_test_pdf(input_file, 5)

    widget.input_file = input_file
    widget.output_file = tmp_path / "modified.pdf"
    widget.range_input.setText("1-10")

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args),
    )

    widget.delete_file()

    assert len(messages) == 1
    assert messages[0][1] == "Invalid input"


def test_delete_file_failure(qtbot, tmp_path, monkeypatch):
    widget = DeleteWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "modified.pdf"

    create_test_pdf(input_file)

    widget.input_file = input_file
    widget.output_file = output_file
    widget.range_input.setText("2")

    def fake_delete(*args, **kwargs):
        raise RuntimeError("Delete failed")

    monkeypatch.setattr(
        "gui.delete_widget.delete_pages",
        fake_delete,
    )

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "critical",
        lambda *args: messages.append(args),
    )

    widget.delete_file()

    assert len(messages) == 1
    assert messages[0][1] == "Delete failed"