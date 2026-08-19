from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.merger import merge_pdfs


class PdfListWidget(QListWidget):
    """PDF list that supports external file drops and internal reordering."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Allow files to be dragged from the file manager into the list.
        self.setAcceptDrops(True)

        # Allow items inside the list to be dragged to change their order.
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Internal dragging is always allowed for reordering.
        if event.source() is self:
            event.acceptProposedAction()
            return

        # External files are accepted only when at least one PDF is included.
        if event.mimeData().hasUrls():
            has_pdf = any(
                url.isLocalFile()
                and Path(url.toLocalFile()).suffix.lower() == ".pdf"
                for url in event.mimeData().urls()
            )

            if has_pdf:
                event.acceptProposedAction()
                return

        event.ignore()

    def dragMoveEvent(self, event):
        # Internal dragging is always allowed for reordering.
        if event.source() is self:
            event.acceptProposedAction()
            return

        # External files are accepted only when at least one PDF is included.
        if event.mimeData().hasUrls():
            has_pdf = any(
                url.isLocalFile()
                and Path(url.toLocalFile()).suffix.lower() == ".pdf"
                for url in event.mimeData().urls()
            )

            if has_pdf:
                event.acceptProposedAction()
                return

        event.ignore()

    def dropEvent(self, event: QDropEvent):
        # Internal drag: let QListWidget move the item first.
        if event.source() is self:
            super().dropEvent(event)

            # Update the owner's PDF list after the visual order changes.
            parent = self.parentWidget()

            if isinstance(parent, MergeWidget):
                parent.sync_pdf_files()

            return

        # External file drop.
        if event.mimeData().hasUrls():
            parent = self.parentWidget()

            if isinstance(parent, MergeWidget):
                parent.add_dropped_files(event.mimeData().urls())

            event.acceptProposedAction()
            return

        event.ignore()


class MergeWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Keep the selected PDF paths as the widget's internal state.
        self.pdf_files: list[Path] = []

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Merge PDF")
        layout.addWidget(title)

        self.file_list = PdfListWidget(self)
        layout.addWidget(self.file_list)

        button_layout = QHBoxLayout()

        add_button = QPushButton("Add PDF")
        add_button.clicked.connect(self.add_pdf)
        button_layout.addWidget(add_button)

        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(remove_button)

        up_button = QPushButton("Move Up")
        up_button.clicked.connect(self.move_up)
        button_layout.addWidget(up_button)

        down_button = QPushButton("Move Down")
        down_button.clicked.connect(self.move_down)
        button_layout.addWidget(down_button)

        layout.addLayout(button_layout)

        output_layout = QHBoxLayout()

        self.output_label = QLabel("Output: Not selected")
        output_layout.addWidget(self.output_label)

        output_button = QPushButton("Choose Output")
        output_button.clicked.connect(self.choose_output)
        output_layout.addWidget(output_button)

        layout.addLayout(output_layout)

        merge_button = QPushButton("Merge PDF")
        merge_button.clicked.connect(self.merge_files)
        layout.addWidget(merge_button)

        self.setLayout(layout)

        self.output_file: Path | None = None

    def add_pdf(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF files",
            "",
            "PDF Files (*.pdf)",
        )

        self.add_pdf_files(files)

    def add_pdf_files(self, files: list[str]):
        """Add PDF files while preventing duplicates."""

        for file in files:
            path = Path(file)

            if path.suffix.lower() != ".pdf":
                continue

            # Avoid adding the same PDF more than once.
            if path not in self.pdf_files:
                self.pdf_files.append(path)
                self.add_list_item(path)

    def add_dropped_files(self, urls):
        """Convert dropped local URLs into PDF file paths."""

        files = []

        for url in urls:
            if not url.isLocalFile():
                continue

            files.append(url.toLocalFile())

        self.add_pdf_files(files)

    def sync_pdf_files(self):
        """Synchronize the internal file order with the visible list."""

        self.pdf_files = [
            Path(self.file_list.item(index).data(Qt.ItemDataRole.UserRole))
            for index in range(self.file_list.count())
        ]

    def add_list_item(self, path: Path):
        """Add a list item while storing its full file path."""

        item = QListWidgetItem(path.name)
        item.setData(Qt.ItemDataRole.UserRole, str(path))

        self.file_list.addItem(item)

    def remove_selected(self):
        row = self.file_list.currentRow()

        if row < 0:
            return

        self.file_list.takeItem(row)
        self.pdf_files.pop(row)

    def move_up(self):
        row = self.file_list.currentRow()

        if row <= 0:
            return

        # Keep the internal file order synchronized with the displayed list.
        self.pdf_files[row - 1], self.pdf_files[row] = (
            self.pdf_files[row],
            self.pdf_files[row - 1],
        )

        item = self.file_list.takeItem(row)
        self.file_list.insertItem(row - 1, item)
        self.file_list.setCurrentRow(row - 1)

    def move_down(self):
        row = self.file_list.currentRow()

        if row < 0 or row >= len(self.pdf_files) - 1:
            return

        # Keep the internal file order synchronized with the displayed list.
        self.pdf_files[row + 1], self.pdf_files[row] = (
            self.pdf_files[row],
            self.pdf_files[row + 1],
        )

        item = self.file_list.takeItem(row)
        self.file_list.insertItem(row + 1, item)
        self.file_list.setCurrentRow(row + 1)

    def choose_output(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save merged PDF",
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.output_file = Path(file)
        self.output_label.setText(f"Output: {self.output_file}")

    def merge_files(self):
        if not self.pdf_files:
            QMessageBox.warning(
                self,
                "No PDF files",
                "Please add at least one PDF file.",
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
            # Reuse the existing PDF merge logic instead of implementing
            # PDF processing directly in the GUI layer.
            merge_pdfs(self.pdf_files, self.output_file)

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Merge failed",
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            "Success",
            "PDF files merged successfully.",
        )