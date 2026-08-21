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

from app.splitter import (
    get_page_count,
    split_pdf,
    validate_page_ranges,
)
from gui.i18n import LanguageManager


class SplitWidget(QWidget):
    def __init__(
        self,
        language_manager: LanguageManager | None = None,
    ):
        super().__init__()

        # Use the shared language manager or English for standalone tests.
        self.language = language_manager or LanguageManager("en")

        self.input_file: Path | None = None
        self.output_dir: Path | None = None

        # Allow PDF files to be dragged into the widget.
        self.setAcceptDrops(True)

        self.setup_ui()

    def set_input_file(self, path: Path):

        self.input_file = path
        self.input_label.setText(
            f"{self.language.get('split.input_prefix')}: "
            f"{path.name}"
        )

    def add_dropped_file(self, path: Path):

        if path.suffix.lower() != ".pdf":
            return

        self.set_input_file(path)

    def _has_pdf_files(self, event) -> bool:

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
        # Only allow dragging PDF files over the widget.
        if self._has_pdf_files(event):
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

            # Split only requires one input PDF.
            break

        event.acceptProposedAction()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.title_label = QLabel(
            self.language.get("split.title")
        )
        self.title_label.setObjectName("pageTitle")
        layout.addWidget(self.title_label)

        self.description_label = QLabel(
            self.language.get("split.description")
        )
        layout.addWidget(self.description_label)

        self.input_title = QLabel(
            self.language.get("split.input_pdf")
        )
        self.input_title.setObjectName("sectionTitle")
        layout.addWidget(self.input_title)

        input_layout = QHBoxLayout()

        self.input_label = QLabel(
            f"{self.language.get('split.input_prefix')}: "
            f"{self.language.get('common.not_selected')}"
        )
        self.input_label.setObjectName("outputLabel")
        input_layout.addWidget(self.input_label)

        self.input_button = QPushButton(
            self.language.get("split.choose_pdf")
        )
        self.input_button.clicked.connect(self.choose_pdf)
        input_layout.addWidget(self.input_button)

        layout.addLayout(input_layout)

        self.range_title = QLabel(
            self.language.get("split.page_ranges")
        )
        self.range_title.setObjectName("sectionTitle")
        layout.addWidget(self.range_title)

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText(
            self.language.get("split.range_placeholder")
        )
        layout.addWidget(self.range_input)

        self.output_title = QLabel(
            self.language.get("split.output_folder")
        )
        self.output_title.setObjectName("sectionTitle")
        layout.addWidget(self.output_title)

        output_layout = QHBoxLayout()

        self.output_label = QLabel(
            f"{self.language.get('split.output_prefix')}: "
            f"{self.language.get('common.not_selected')}"
        )
        self.output_label.setObjectName("outputLabel")
        output_layout.addWidget(self.output_label)

        self.output_button = QPushButton(
            self.language.get("split.choose_output")
        )
        self.output_button.clicked.connect(self.choose_output)
        output_layout.addWidget(self.output_button)

        layout.addLayout(output_layout)

        self.split_button = QPushButton(
            self.language.get("split.split_pdf")
        )
        self.split_button.setObjectName("primaryButton")
        self.split_button.clicked.connect(self.split_file)
        layout.addWidget(self.split_button)

        layout.addStretch()

        self.setLayout(layout)

    def choose_pdf(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            self.language.get("split.choose_pdf"),
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.set_input_file(Path(file))

    def choose_output(self):

        directory = QFileDialog.getExistingDirectory(
            self,
            self.language.get("split.choose_output"),
        )

        if not directory:
            return

        self.output_dir = Path(directory)

        self.output_label.setText(
            f"{self.language.get('split.output_prefix')}: "
            f"{self.output_dir}"
        )

    def split_file(self):

        if self.input_file is None:
            QMessageBox.warning(
                self,
                self.language.get("split.input_not_selected"),
                self.language.get("split.choose_pdf_message"),
            )
            return

        page_range_text = self.range_input.text().strip()

        if not page_range_text:
            QMessageBox.warning(
                self,
                self.language.get("split.range_not_entered"),
                self.language.get("split.enter_ranges_message"),
            )
            return

        if self.output_dir is None:
            QMessageBox.warning(
                self,
                self.language.get("split.output_not_selected"),
                self.language.get("split.choose_output_message"),
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

            # Reuse the existing PDF splitting logic.
            output_files = split_pdf(
                self.input_file,
                self.output_dir,
                page_ranges,
            )

        except ValueError as exc:
            QMessageBox.warning(
                self,
                self.language.get("split.invalid_input"),
                str(exc),
            )
            return

        except Exception as exc:
            QMessageBox.critical(
                self,
                self.language.get("split.failed"),
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            self.language.get("common.success"),
            self.language.get("split.success").format(
                count=len(output_files)
            ),
        )

    @staticmethod
    def parse_page_ranges(
        text: str,
    ) -> list[tuple[int, int]]:

        ranges = []

        # Convert inputs such as "1-3, 5, 7-9".
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

        self.title_label.setText(
            self.language.get("split.title")
        )

        self.description_label.setText(
            self.language.get("split.description")
        )

        self.input_title.setText(
            self.language.get("split.input_pdf")
        )

        self.input_button.setText(
            self.language.get("split.choose_pdf")
        )

        self.range_title.setText(
            self.language.get("split.page_ranges")
        )

        self.range_input.setPlaceholderText(
            self.language.get("split.range_placeholder")
        )

        self.output_title.setText(
            self.language.get("split.output_folder")
        )

        self.output_button.setText(
            self.language.get("split.choose_output")
        )

        self.split_button.setText(
            self.language.get("split.split_pdf")
        )

        # Keep the currently selected path unchanged.
        if self.input_file is None:
            self.input_label.setText(
                f"{self.language.get('split.input_prefix')}: "
                f"{self.language.get('common.not_selected')}"
            )
        else:
            self.input_label.setText(
                f"{self.language.get('split.input_prefix')}: "
                f"{self.input_file.name}"
            )

        if self.output_dir is None:
            self.output_label.setText(
                f"{self.language.get('split.output_prefix')}: "
                f"{self.language.get('common.not_selected')}"
            )
        else:
            self.output_label.setText(
                f"{self.language.get('split.output_prefix')}: "
                f"{self.output_dir}"
            )