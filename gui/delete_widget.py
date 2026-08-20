from pathlib import Path

from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.page_manager import delete_pages
from app.splitter import (
    get_page_count,
    validate_page_ranges,
)
from gui.i18n import LanguageManager


class DeleteWidget(QWidget):
    def __init__(
        self,
        language_manager: LanguageManager | None = None,
    ):
        super().__init__()

        # Use the shared language manager or English for standalone tests.
        self.language = language_manager or LanguageManager("en")

        self.input_file: Path | None = None
        self.output_file: Path | None = None

        # Allow PDF files to be dragged into the widget.
        self.setAcceptDrops(True)

        self.setup_ui()

    def add_dropped_file(self, path: Path):
        """Accept only PDF files as delete input."""

        if path.suffix.lower() != ".pdf":
            return

        self.set_input_file(path)

    def set_input_file(self, path: Path):
        """Set the input PDF and update the displayed filename."""

        self.input_file = path
        self.input_label.setText(
            f"{self.language.get('delete.input_prefix')}: "
            f"{path.name}"
        )

    def _has_pdf_files(self, event) -> bool:
        """Return whether the drag contains at least one PDF."""

        if not event.mimeData().hasUrls():
            return False

        return any(
            url.isLocalFile()
            and Path(url.toLocalFile()).suffix.lower() == ".pdf"
            for url in event.mimeData().urls()
        )

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Only accept external drops containing PDF files.
        if self._has_pdf_files(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Only allow PDF files to be dragged over the widget.
        if self._has_pdf_files(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Use the first dropped PDF as the input file."""

        if not event.mimeData().hasUrls():
            event.ignore()
            return

        for url in event.mimeData().urls():
            if not url.isLocalFile():
                continue

            path = Path(url.toLocalFile())

            if path.suffix.lower() != ".pdf":
                continue

            self.add_dropped_file(path)

            # Delete only needs one input PDF.
            break

        event.acceptProposedAction()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.title_label = QLabel(
            self.language.get("delete.title")
        )
        self.title_label.setObjectName("pageTitle")
        layout.addWidget(self.title_label)

        self.description_label = QLabel(
            self.language.get("delete.description")
        )
        layout.addWidget(self.description_label)

        self.input_title = QLabel(
            self.language.get("delete.input_pdf")
        )
        self.input_title.setObjectName("sectionTitle")
        layout.addWidget(self.input_title)

        input_layout = QHBoxLayout()

        self.input_label = QLabel(
            f"{self.language.get('delete.input_prefix')}: "
            f"{self.language.get('common.not_selected')}"
        )
        self.input_label.setObjectName("outputLabel")
        input_layout.addWidget(self.input_label)

        self.input_button = QPushButton(
            self.language.get("delete.choose_pdf")
        )
        self.input_button.clicked.connect(self.choose_pdf)
        input_layout.addWidget(self.input_button)

        layout.addLayout(input_layout)

        self.pages_title = QLabel(
            self.language.get("delete.pages_to_delete")
        )
        self.pages_title.setObjectName("sectionTitle")
        layout.addWidget(self.pages_title)

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText(
            self.language.get("delete.range_placeholder")
        )
        layout.addWidget(self.range_input)

        self.output_title = QLabel(
            self.language.get("delete.output")
        )
        self.output_title.setObjectName("sectionTitle")
        layout.addWidget(self.output_title)

        output_layout = QHBoxLayout()

        self.output_label = QLabel(
            f"{self.language.get('delete.output_prefix')}: "
            f"{self.language.get('common.not_selected')}"
        )
        self.output_label.setObjectName("outputLabel")
        output_layout.addWidget(self.output_label)

        self.output_button = QPushButton(
            self.language.get("delete.choose_output")
        )
        self.output_button.clicked.connect(self.choose_output)
        output_layout.addWidget(self.output_button)

        layout.addLayout(output_layout)

        self.delete_button = QPushButton(
            self.language.get("delete.delete_pages")
        )
        self.delete_button.setObjectName("dangerButton")
        self.delete_button.clicked.connect(self.delete_file)
        layout.addWidget(self.delete_button)

        layout.addStretch()

        self.setLayout(layout)

    def choose_pdf(self):
        """Select the input PDF through a file dialog."""

        file, _ = QFileDialog.getOpenFileName(
            self,
            self.language.get("delete.choose_pdf"),
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.set_input_file(Path(file))

    def choose_output(self):
        """Select the output PDF file."""

        file, _ = QFileDialog.getSaveFileName(
            self,
            self.language.get("delete.choose_output"),
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.output_file = Path(file)

        self.output_label.setText(
            f"{self.language.get('delete.output_prefix')}: "
            f"{self.output_file}"
        )

    def delete_file(self):
        """Validate input and delete the selected pages."""

        if self.input_file is None:
            QMessageBox.warning(
                self,
                self.language.get("delete.input_not_selected"),
                self.language.get("delete.choose_pdf_message"),
            )
            return

        page_range_text = self.range_input.text().strip()

        if not page_range_text:
            QMessageBox.warning(
                self,
                self.language.get("delete.pages_not_entered"),
                self.language.get("delete.enter_pages_message"),
            )
            return

        if self.output_file is None:
            QMessageBox.warning(
                self,
                self.language.get("delete.output_not_selected"),
                self.language.get("delete.choose_output_message"),
            )
            return

        try:
            # Convert the user's input into page range tuples.
            page_ranges = self.parse_page_ranges(
                page_range_text
            )

            page_count = get_page_count(
                self.input_file
            )

            # Validate ranges before modifying the PDF.
            validate_page_ranges(
                page_ranges,
                page_count,
            )

            # Reuse the existing page deletion logic.
            delete_pages(
                self.input_file,
                self.output_file,
                page_ranges,
            )

        except ValueError as exc:
            QMessageBox.warning(
                self,
                self.language.get("delete.invalid_input"),
                str(exc),
            )
            return

        except Exception as exc:
            QMessageBox.critical(
                self,
                self.language.get("delete.failed"),
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            self.language.get("common.success"),
            self.language.get("delete.success"),
        )

    @staticmethod
    def parse_page_ranges(
        text: str,
    ) -> list[tuple[int, int]]:
        """Convert page range text into page range tuples."""

        ranges = []

        # Convert inputs such as "2, 5-7, 10".
        for part in text.split(","):
            part = part.strip()

            if not part:
                continue

            if "-" in part:
                start, end = part.split("-", 1)

                start_page = int(start.strip())
                end_page = int(end.strip())
            else:
                start_page = int(part)
                end_page = start_page

            ranges.append((start_page, end_page))

        if not ranges:
            raise ValueError(
                "No valid page ranges were entered."
            )

        return ranges

    def refresh_ui(self):
        """Refresh all visible text using the current language."""

        self.title_label.setText(
            self.language.get("delete.title")
        )

        self.description_label.setText(
            self.language.get("delete.description")
        )

        self.input_title.setText(
            self.language.get("delete.input_pdf")
        )

        self.input_button.setText(
            self.language.get("delete.choose_pdf")
        )

        self.pages_title.setText(
            self.language.get("delete.pages_to_delete")
        )

        self.range_input.setPlaceholderText(
            self.language.get("delete.range_placeholder")
        )

        self.output_title.setText(
            self.language.get("delete.output")
        )

        self.output_button.setText(
            self.language.get("delete.choose_output")
        )

        self.delete_button.setText(
            self.language.get("delete.delete_pages")
        )

        if self.input_file is None:
            self.input_label.setText(
                f"{self.language.get('delete.input_prefix')}: "
                f"{self.language.get('common.not_selected')}"
            )
        else:
            self.input_label.setText(
                f"{self.language.get('delete.input_prefix')}: "
                f"{self.input_file.name}"
            )

        if self.output_file is None:
            self.output_label.setText(
                f"{self.language.get('delete.output_prefix')}: "
                f"{self.language.get('common.not_selected')}"
            )
        else:
            self.output_label.setText(
                f"{self.language.get('delete.output_prefix')}: "
                f"{self.output_file}"
            )