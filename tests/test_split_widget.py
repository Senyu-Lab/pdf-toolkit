from pathlib import Path

import pymupdf
from PySide6.QtWidgets import QMessageBox

from gui.split_widget import SplitWidget


def create_test_pdf(path: Path, page_count: int = 5):
    doc = pymupdf.open()

    for _ in range(page_count):
        doc.new_page()

    doc.save(path)
    doc.close()


def test_parse_page_ranges():
    assert SplitWidget.parse_page_ranges("1-3,5-7") == [
        (1, 3),
        (5, 7),
    ]


def test_parse_single_page():
    assert SplitWidget.parse_page_ranges("3") == [
        (3, 3),
    ]


def test_parse_page_ranges_with_spaces():
    assert SplitWidget.parse_page_ranges("1-3, 5, 7-9") == [
        (1, 3),
        (5, 5),
        (7, 9),
    ]


def test_parse_page_ranges_empty():
    try:
        SplitWidget.parse_page_ranges("")
        assert False
    except ValueError as exc:
        assert "No valid page ranges" in str(exc)


def test_choose_pdf(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    create_test_pdf(input_file)

    monkeypatch.setattr(
        "gui.split_widget.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (
            str(input_file),
            "PDF Files (*.pdf)",
        ),
    )

    widget.choose_pdf()

    assert widget.input_file == input_file
    assert widget.input_label.text() == "PDF: input.pdf"


def test_choose_output(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    monkeypatch.setattr(
        "gui.split_widget.QFileDialog.getExistingDirectory",
        lambda *args, **kwargs: str(output_dir),
    )

    widget.choose_output()

    assert widget.output_dir == output_dir
    assert str(output_dir) in widget.output_label.text()


def test_choose_pdf_cancelled(qtbot, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    monkeypatch.setattr(
        "gui.split_widget.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: ("", ""),
    )

    widget.choose_pdf()

    assert widget.input_file is None


def test_choose_output_cancelled(qtbot, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    monkeypatch.setattr(
        "gui.split_widget.QFileDialog.getExistingDirectory",
        lambda *args, **kwargs: "",
    )

    widget.choose_output()

    assert widget.output_dir is None


def test_split_without_pdf(qtbot, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args[2]),
    )

    widget.split_file()

    assert messages
    assert "choose a PDF file" in messages[0]


def test_split_without_page_ranges(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    create_test_pdf(input_file)

    widget.input_file = input_file

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args[2]),
    )

    widget.split_file()

    assert messages
    assert "page ranges" in messages[0].lower()


def test_split_without_output(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    create_test_pdf(input_file)

    widget.input_file = input_file
    widget.range_input.setText("1-2")

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args[2]),
    )

    widget.split_file()

    assert messages
    assert "output" in messages[0].lower()


def test_split_success(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    create_test_pdf(input_file, 5)

    widget.input_file = input_file
    widget.output_dir = output_dir
    widget.range_input.setText("1-2,4-5")

    called = {}

    def fake_get_page_count(path):
        return 5

    def fake_validate_page_ranges(page_ranges, page_count):
        called["validated"] = (page_ranges, page_count)

    def fake_split(input_file_arg, output_dir_arg, page_ranges):
        called["input_file"] = input_file_arg
        called["output_dir"] = output_dir_arg
        called["page_ranges"] = page_ranges

        return [
            output_dir_arg / "split_1.pdf",
            output_dir_arg / "split_2.pdf",
        ]

    monkeypatch.setattr(
        "gui.split_widget.get_page_count",
        fake_get_page_count,
    )

    monkeypatch.setattr(
        "gui.split_widget.validate_page_ranges",
        fake_validate_page_ranges,
    )

    monkeypatch.setattr(
        "gui.split_widget.split_pdf",
        fake_split,
    )

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args: messages.append(args[2]),
    )

    widget.split_file()

    assert called["input_file"] == input_file
    assert called["output_dir"] == output_dir
    assert called["page_ranges"] == [(1, 2), (4, 5)]
    assert called["validated"] == ([(1, 2), (4, 5)], 5)

    assert messages
    assert "2 file(s)" in messages[0]


def test_split_invalid_page_range(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    create_test_pdf(input_file, 5)

    widget.input_file = input_file
    widget.output_dir = output_dir
    widget.range_input.setText("1-10")

    messages = []

    monkeypatch.setattr(
        "gui.split_widget.validate_page_ranges",
        lambda *args: (_ for _ in ()).throw(
            ValueError("Page range is out of bounds.")
        ),
    )

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args[2]),
    )

    widget.split_file()

    assert messages
    assert "out of bounds" in messages[0]


def test_split_failure(qtbot, tmp_path, monkeypatch):
    widget = SplitWidget()
    qtbot.addWidget(widget)

    input_file = tmp_path / "input.pdf"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    create_test_pdf(input_file)

    widget.input_file = input_file
    widget.output_dir = output_dir
    widget.range_input.setText("1-2")

    monkeypatch.setattr(
        "gui.split_widget.get_page_count",
        lambda path: 5,
    )

    monkeypatch.setattr(
        "gui.split_widget.validate_page_ranges",
        lambda *args: None,
    )

    def fake_split(*args, **kwargs):
        raise RuntimeError("Split failed")

    monkeypatch.setattr(
        "gui.split_widget.split_pdf",
        fake_split,
    )

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "critical",
        lambda *args: messages.append(args[2]),
    )

    widget.split_file()

    assert messages
    assert "Split failed" in messages[0]