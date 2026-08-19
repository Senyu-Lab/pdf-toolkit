from pathlib import Path

from PySide6.QtCore import QMimeData, QUrl
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

from app.splitter import (
    get_page_count,
    split_pdf,
    validate_page_ranges,
)


class SplitWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.input_file: Path | None = None
        self.output_dir: Path | None = None

        self.setAcceptDrops(True)

        self.setup_ui()

    def set_input_file(self, path: Path):
        # Keep the selected PDF path and displayed filename synchronized.
        self.input_file = path
        self.input_label.setText(f"PDF: {path.name}")

    def add_dropped_file(self, path: Path):
        # Split only accepts PDF files as input.
        if path.suffix.lower() != ".pdf":
            return

        self.set_input_file(path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if not event.mimeData().hasUrls():
            event.ignore()
            return

        has_pdf = any(
            url.isLocalFile()
            and Path(url.toLocalFile()).suffix.lower() == ".pdf"
            for url in event.mimeData().urls()
        )

        if has_pdf:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if not event.mimeData().hasUrls():
            event.ignore()
            return

        has_pdf = any(
            url.isLocalFile()
            and Path(url.toLocalFile()).suffix.lower() == ".pdf"
            for url in event.mimeData().urls()
        )

        if has_pdf:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
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

            # Split only needs one input PDF.
            break

        event.acceptProposedAction()



    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Split PDF")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        description = QLabel(
            "Select a PDF, enter page ranges, and split it into separate files."
        )
        layout.addWidget(description)

        section_title = QLabel("Input PDF")
        section_title.setObjectName("sectionTitle")
        layout.addWidget(section_title)

        input_layout = QHBoxLayout()

        self.input_label = QLabel("PDF: Not selected")
        self.input_label.setObjectName("outputLabel")
        input_layout.addWidget(self.input_label)

        input_button = QPushButton("Choose PDF")
        input_button.clicked.connect(self.choose_pdf)
        input_layout.addWidget(input_button)

        layout.addLayout(input_layout)

        range_title = QLabel("Page Ranges")
        range_title.setObjectName("sectionTitle")
        layout.addWidget(range_title)

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText(
            "Example: 1-3, 5-7"
        )
        layout.addWidget(self.range_input)

        output_title = QLabel("Output Folder")
        output_title.setObjectName("sectionTitle")
        layout.addWidget(output_title)

        output_layout = QHBoxLayout()

        self.output_label = QLabel("Output: Not selected")
        self.output_label.setObjectName("outputLabel")
        output_layout.addWidget(self.output_label)

        output_button = QPushButton("Choose Output Folder")
        output_button.clicked.connect(self.choose_output)
        output_layout.addWidget(output_button)

        layout.addLayout(output_layout)

        split_button = QPushButton("Split PDF")
        split_button.setObjectName("primaryButton")
        split_button.clicked.connect(self.split_file)
        layout.addWidget(split_button)

        layout.addStretch()

        self.setLayout(layout)



    def choose_pdf(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF file",
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.set_input_file(Path(file))

    def choose_output(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select output folder",
        )

        if not directory:
            return

        self.output_dir = Path(directory)
        self.output_label.setText(
            f"Output: {self.output_dir}"
        )

    def split_file(self):
        if self.input_file is None:
            QMessageBox.warning(
                self,
                "PDF not selected",
                "Please choose a PDF file.",
            )
            return

        page_range_text = self.range_input.text().strip()

        if not page_range_text:
            QMessageBox.warning(
                self,
                "Page ranges not entered",
                "Please enter page ranges.",
            )
            return

        if self.output_dir is None:
            QMessageBox.warning(
                self,
                "Output not selected",
                "Please choose an output folder.",
            )
            return

        try:
            # Convert the user's page range input into page range tuples.
            page_ranges = self.parse_page_ranges(
                page_range_text
            )

            page_count = get_page_count(
                self.input_file
            )

            # Validate the requested ranges before modifying the PDF.
            validate_page_ranges(
                page_ranges,
                page_count,
            )

            # Reuse the existing PDF splitting logic.
            output_files = split_pdf(
                self.input_file,
                self.output_dir,
                page_ranges,
            )

        except ValueError as exc:
            QMessageBox.warning(
                self,
                "Invalid input",
                str(exc),
            )
            return

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Split failed",
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            "Success",
            f"PDF split successfully into {len(output_files)} file(s).",
        )

    @staticmethod
    def parse_page_ranges(
        text: str,
    ) -> list[tuple[int, int]]:
        ranges = []

        # Convert inputs such as "1-3, 5, 7-9" into page range tuples.
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