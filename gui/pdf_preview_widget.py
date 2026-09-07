from pathlib import Path

import fitz
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from gui.i18n import LanguageManager


class PdfPreviewWidget(QWidget):
    def __init__(
        self,
        language_manager: LanguageManager | None = None,
    ):
        super().__init__()

        self.language = language_manager or LanguageManager("en")

        self.document: fitz.Document | None = None
        self.file_path: Path | None = None
        self.current_page = 0
        self.zoom_factor = 1.0

        self.setup_ui()
        self.refresh_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel()
        self.title_label.setObjectName("sectionTitle")
        layout.addWidget(self.title_label)

        self.file_label = QLabel()
        self.file_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(self.file_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.page_label = QLabel()
        self.page_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.scroll_area.setWidget(self.page_label)

        layout.addWidget(self.scroll_area)

        navigation_layout = QHBoxLayout()

        self.previous_button = QPushButton()
        self.previous_button.clicked.connect(
            self.previous_page
        )
        navigation_layout.addWidget(self.previous_button)

        self.page_indicator = QLabel()
        self.page_indicator.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        navigation_layout.addWidget(self.page_indicator)

        self.next_button = QPushButton()
        self.next_button.clicked.connect(
            self.next_page
        )
        navigation_layout.addWidget(self.next_button)

        layout.addLayout(navigation_layout)

        zoom_layout = QHBoxLayout()

        self.zoom_out_button = QPushButton()
        self.zoom_out_button.clicked.connect(
            self.zoom_out
        )
        zoom_layout.addWidget(self.zoom_out_button)

        self.fit_button = QPushButton()
        self.fit_button.clicked.connect(
            self.fit_to_window
        )
        zoom_layout.addWidget(self.fit_button)

        self.zoom_in_button = QPushButton()
        self.zoom_in_button.clicked.connect(
            self.zoom_in
        )
        zoom_layout.addWidget(self.zoom_in_button)

        layout.addLayout(zoom_layout)

        self.setLayout(layout)

    def load_pdf(self, path: Path):
        self.close_document()

        try:
            self.document = fitz.open(path)
        except Exception:
            self.file_path = None
            self.page_label.clear()
            self.page_indicator.clear()
            self.file_label.clear()
            self._update_navigation()
            return

        if self.document.page_count == 0:
            self.close_document()
            return

        self.file_path = path
        self.current_page = 0
        self.zoom_factor = 1.0

        self.file_label.setText(path.name)

        self.render_page()

    def close_document(self):
        if self.document is not None:
            self.document.close()

        self.document = None
        self.file_path = None
        self.current_page = 0
        self.zoom_factor = 1.0

    def render_page(self):
        if self.document is None:
            return

        page = self.document.load_page(
            self.current_page
        )

        matrix = fitz.Matrix(
            self.zoom_factor,
            self.zoom_factor,
        )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format.Format_RGB888,
        )

        self.page_label.setPixmap(
            QPixmap.fromImage(image.copy())
        )

        self.page_indicator.setText(
            f"{self.current_page + 1} / "
            f"{self.document.page_count}"
        )

        self._update_navigation()

    def previous_page(self):
        if self.document is None:
            return

        if self.current_page <= 0:
            return

        self.current_page -= 1
        self.render_page()

    def next_page(self):
        if self.document is None:
            return

        if self.current_page >= self.document.page_count - 1:
            return

        self.current_page += 1
        self.render_page()

    def zoom_in(self):
        if self.document is None:
            return

        self.zoom_factor *= 1.2
        self.render_page()

    def zoom_out(self):
        if self.document is None:
            return

        self.zoom_factor /= 1.2
        self.render_page()

    def fit_to_window(self):
        if self.document is None:
            return

        page = self.document.load_page(
            self.current_page
        )

        page_width = page.rect.width
        page_height = page.rect.height

        viewport = self.scroll_area.viewport()

        available_width = max(
            viewport.width() - 20,
            1,
        )
        available_height = max(
            viewport.height() - 20,
            1,
        )

        width_scale = (
            available_width / page_width
        )
        height_scale = (
            available_height / page_height
        )

        self.zoom_factor = min(
            width_scale,
            height_scale,
        )

        self.render_page()

    def _update_navigation(self):
        has_document = self.document is not None

        self.previous_button.setEnabled(
            has_document and self.current_page > 0
        )

        self.next_button.setEnabled(
            has_document
            and self.current_page
            < self.document.page_count - 1
        )

        self.zoom_in_button.setEnabled(
            has_document
        )

        self.zoom_out_button.setEnabled(
            has_document
        )

        self.fit_button.setEnabled(
            has_document
        )

    def refresh_ui(self):
        self.title_label.setText(
            self.language.get("preview.title")
        )
        self.previous_button.setText(
            self.language.get("preview.previous")
        )
        self.next_button.setText(
            self.language.get("preview.next")
        )
        self.zoom_out_button.setText(
            self.language.get("preview.zoom_out")
        )
        self.fit_button.setText(
            self.language.get("preview.fit")
        )
        self.zoom_in_button.setText(
            self.language.get("preview.zoom_in")
        )

        if self.file_path is None:
            self.file_label.setText(
                self.language.get("preview.no_file")
            )

    def closeEvent(self, event):
        self.close_document()
        event.accept()