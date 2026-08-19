from pathlib import Path

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
from app.splitter import get_page_count, validate_page_ranges


class DeleteWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.input_file: Path | None = None
        self.output_file: Path | None = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Delete Pages")
        layout.addWidget(title)

        input_layout = QHBoxLayout()

        self.input_label = QLabel("PDF: Not selected")
        input_layout.addWidget(self.input_label)

        input_button = QPushButton("Choose PDF")
        input_button.clicked.connect(self.choose_pdf)
        input_layout.addWidget(input_button)

        layout.addLayout(input_layout)

        range_layout = QHBoxLayout()

        range_label = QLabel("Pages to delete:")
        range_layout.addWidget(range_label)

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("Example: 2,4-6")
        range_layout.addWidget(self.range_input)

        layout.addLayout(range_layout)

        output_layout = QHBoxLayout()

        self.output_label = QLabel("Output: Not selected")
        output_layout.addWidget(self.output_label)

        output_button = QPushButton("Choose Output")
        output_button.clicked.connect(self.choose_output)
        output_layout.addWidget(output_button)

        layout.addLayout(output_layout)

        delete_button = QPushButton("Delete Pages")
        delete_button.clicked.connect(self.delete_file)
        layout.addWidget(delete_button)

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

        self.input_file = Path(file)
        self.input_label.setText(f"PDF: {self.input_file.name}")

    def choose_output(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save modified PDF",
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.output_file = Path(file)
        self.output_label.setText(f"Output: {self.output_file}")

    def delete_file(self):
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
                "Pages not entered",
                "Please enter pages to delete.",
            )
            return

        if self.output_file is None:
            QMessageBox.warning(
                self,
                "Output not selected",
                "Please choose an output file.",
            )
            return

        try:
            page_ranges = self.parse_page_ranges(page_range_text)

            page_count = get_page_count(self.input_file)

            # Validate the ranges before deleting pages to prevent
            # invalid page numbers or deleting the entire document.
            validate_page_ranges(
                page_ranges,
                page_count,
            )

            # Delegate the actual PDF page deletion to the core application logic.
            delete_pages(
                self.input_file,
                self.output_file,
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
                "Delete failed",
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            "Success",
            "Pages deleted successfully.",
        )

    @staticmethod
    def parse_page_ranges(text: str) -> list[tuple[int, int]]:
        ranges = []

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
            raise ValueError("No valid page ranges were entered.")

        return ranges