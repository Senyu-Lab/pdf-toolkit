from pathlib import Path

import fitz
import pytest

from gui.pdf_preview_widget import PdfPreviewWidget


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "sample.pdf"

    document = fitz.open()

    for index in range(3):
        page = document.new_page()
        page.insert_text(
            (72, 72),
            f"Page {index + 1}",
        )

    document.save(pdf_path)
    document.close()

    return pdf_path


def test_initial_state(qtbot):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    assert widget.document is None
    assert widget.file_path is None
    assert widget.current_page == 0


def test_load_pdf(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)

    assert widget.document is not None
    assert widget.file_path == sample_pdf
    assert widget.current_page == 0
    assert widget.document.page_count == 3


def test_load_pdf_displays_first_page(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)

    assert widget.page_label.pixmap() is not None
    assert not widget.page_label.pixmap().isNull()


def test_next_page(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)
    widget.next_page()

    assert widget.current_page == 1


def test_previous_page(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)
    widget.next_page()
    widget.previous_page()

    assert widget.current_page == 0


def test_previous_page_stays_at_first_page(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)
    widget.previous_page()

    assert widget.current_page == 0


def test_next_page_stays_at_last_page(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)

    widget.next_page()
    widget.next_page()
    widget.next_page()

    assert widget.current_page == 2


def test_zoom_in(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)

    original_zoom = widget.zoom_factor

    widget.zoom_in()

    assert widget.zoom_factor > original_zoom


def test_zoom_out(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)

    original_zoom = widget.zoom_factor

    widget.zoom_out()

    assert widget.zoom_factor < original_zoom


def test_fit_to_window(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.resize(800, 600)
    widget.show()

    widget.load_pdf(sample_pdf)
    widget.fit_to_window()

    assert widget.zoom_factor > 0


def test_invalid_pdf_does_not_crash(qtbot, tmp_path):
    invalid_pdf = tmp_path / "invalid.pdf"
    invalid_pdf.write_text("This is not a PDF.")

    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(invalid_pdf)

    assert widget.document is None
    assert widget.file_path is None


def test_close_document(qtbot, sample_pdf):
    widget = PdfPreviewWidget()
    qtbot.addWidget(widget)

    widget.load_pdf(sample_pdf)
    widget.close_document()

    assert widget.document is None
    assert widget.file_path is None
    assert widget.current_page == 0
    assert widget.zoom_factor == 1.0