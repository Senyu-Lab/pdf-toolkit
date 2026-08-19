from pathlib import Path

import pymupdf
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QFileDialog, QMessageBox

from gui.merge_widget import MergeWidget


def create_test_pdf(path: Path, pages: int = 2):
    doc = pymupdf.open()

    for _ in range(pages):
        doc.new_page()

    doc.save(path)
    doc.close()


def test_add_pdf(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"

    create_test_pdf(pdf1)
    create_test_pdf(pdf2)

    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda *args, **kwargs: (
            [str(pdf1), str(pdf2)],
            "PDF Files (*.pdf)",
        ),
    )

    widget.add_pdf()

    assert widget.pdf_files == [pdf1, pdf2]
    assert widget.file_list.count() == 2
    assert widget.file_list.item(0).text() == "one.pdf"
    assert widget.file_list.item(1).text() == "two.pdf"


def test_add_pdf_does_not_add_duplicates(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf = tmp_path / "test.pdf"
    create_test_pdf(pdf)

    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda *args, **kwargs: (
            [str(pdf), str(pdf)],
            "PDF Files (*.pdf)",
        ),
    )

    widget.add_pdf()

    assert widget.pdf_files == [pdf]
    assert widget.file_list.count() == 1


def test_remove_selected(qtbot, tmp_path):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"

    widget.pdf_files = [pdf1, pdf2]
    widget.file_list.addItems(["one.pdf", "two.pdf"])
    widget.file_list.setCurrentRow(0)

    widget.remove_selected()

    assert widget.pdf_files == [pdf2]
    assert widget.file_list.count() == 1
    assert widget.file_list.item(0).text() == "two.pdf"


def test_move_up(qtbot, tmp_path):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"
    pdf3 = tmp_path / "three.pdf"

    widget.pdf_files = [pdf1, pdf2, pdf3]
    widget.file_list.addItems(
        ["one.pdf", "two.pdf", "three.pdf"]
    )
    widget.file_list.setCurrentRow(1)

    widget.move_up()

    assert widget.pdf_files == [pdf2, pdf1, pdf3]
    assert widget.file_list.item(0).text() == "two.pdf"
    assert widget.file_list.item(1).text() == "one.pdf"
    assert widget.file_list.currentRow() == 0


def test_move_down(qtbot, tmp_path):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"
    pdf3 = tmp_path / "three.pdf"

    widget.pdf_files = [pdf1, pdf2, pdf3]
    widget.file_list.addItems(
        ["one.pdf", "two.pdf", "three.pdf"]
    )
    widget.file_list.setCurrentRow(1)

    widget.move_down()

    assert widget.pdf_files == [pdf1, pdf3, pdf2]
    assert widget.file_list.item(1).text() == "three.pdf"
    assert widget.file_list.item(2).text() == "two.pdf"
    assert widget.file_list.currentRow() == 2


def test_choose_output(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    output_file = tmp_path / "merged.pdf"

    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (
            str(output_file),
            "PDF Files (*.pdf)",
        ),
    )

    widget.choose_output()

    assert widget.output_file == output_file
    assert widget.output_label.text() == f"Output: {output_file}"


def test_merge_files_success(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"
    output = tmp_path / "merged.pdf"

    create_test_pdf(pdf1, 2)
    create_test_pdf(pdf2, 3)

    widget.pdf_files = [pdf1, pdf2]
    widget.output_file = output

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args: messages.append(args),
    )

    widget.merge_files()

    assert output.exists()

    doc = pymupdf.open(output)
    assert len(doc) == 5
    doc.close()

    assert messages


def test_merge_files_without_pdfs(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args),
    )

    widget.merge_files()

    assert len(messages) == 1
    assert "No PDF files" in messages[0][1]


def test_merge_files_without_output(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf = tmp_path / "test.pdf"
    create_test_pdf(pdf)

    widget.pdf_files = [pdf]

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args: messages.append(args),
    )

    widget.merge_files()

    assert len(messages) == 1
    assert "Output not selected" in messages[0][1]


def test_merge_files_failure(qtbot, tmp_path, monkeypatch):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf = tmp_path / "test.pdf"
    output = tmp_path / "merged.pdf"

    widget.pdf_files = [pdf]
    widget.output_file = output

    def fake_merge(*args, **kwargs):
        raise ValueError("Merge failed")

    monkeypatch.setattr(
        "gui.merge_widget.merge_pdfs",
        fake_merge,
    )

    messages = []

    monkeypatch.setattr(
        QMessageBox,
        "critical",
        lambda *args: messages.append(args),
    )

    widget.merge_files()

    assert len(messages) == 1
    assert "Merge failed" in messages[0][2]

def test_add_dropped_pdf_files(qtbot, tmp_path):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "test1.pdf"
    pdf2 = tmp_path / "test2.pdf"

    urls = [
        QUrl.fromLocalFile(str(pdf1)),
        QUrl.fromLocalFile(str(pdf2)),
    ]

    widget.add_dropped_files(urls)

    assert widget.pdf_files == [pdf1, pdf2]
    assert widget.file_list.count() == 2
    assert widget.file_list.item(0).text() == "test1.pdf"
    assert widget.file_list.item(1).text() == "test2.pdf"


def test_add_dropped_non_pdf_files(qtbot, tmp_path):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    txt_file = tmp_path / "test.txt"
    png_file = tmp_path / "test.png"

    urls = [
        QUrl.fromLocalFile(str(txt_file)),
        QUrl.fromLocalFile(str(png_file)),
    ]

    widget.add_dropped_files(urls)

    assert widget.pdf_files == []
    assert widget.file_list.count() == 0


def test_add_dropped_mixed_files(qtbot, tmp_path):
    widget = MergeWidget()
    qtbot.addWidget(widget)

    pdf1 = tmp_path / "test1.pdf"
    txt_file = tmp_path / "test.txt"
    pdf2 = tmp_path / "test2.PDF"
    png_file = tmp_path / "test.png"

    urls = [
        QUrl.fromLocalFile(str(pdf1)),
        QUrl.fromLocalFile(str(txt_file)),
        QUrl.fromLocalFile(str(pdf2)),
        QUrl.fromLocalFile(str(png_file)),
    ]

    widget.add_dropped_files(urls)

    assert widget.pdf_files == [pdf1, pdf2]
    assert widget.file_list.count() == 2
    assert widget.file_list.item(0).text() == "test1.pdf"
    assert widget.file_list.item(1).text() == "test2.PDF"