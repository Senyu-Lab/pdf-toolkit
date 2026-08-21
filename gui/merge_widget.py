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
from gui.i18n import LanguageManager


# PDF list that supports external drops and internal reordering.
class PdfListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Allow files to be dragged into the list.
        self.setAcceptDrops(True)

        # Allow items to be reordered by dragging.
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDropIndicatorShown(True)

    def _has_pdf_files(self, event) -> bool:

        if not event.mimeData().hasUrls():
            return False

        return any(
            url.isLocalFile()
            and Path(url.toLocalFile()).suffix.lower() == ".pdf"
            for url in event.mimeData().urls()
        )

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Internal dragging is always allowed for reordering.
        if event.source() is self:
            event.acceptProposedAction()
            return

        if self._has_pdf_files(event):
            event.acceptProposedAction()
            return

        event.ignore()

    def dragMoveEvent(self, event):
        # Internal dragging is always allowed for reordering.
        if event.source() is self:
            event.acceptProposedAction()
            return

        if self._has_pdf_files(event):
            event.acceptProposedAction()
            return

        event.ignore()

    def dropEvent(self, event: QDropEvent):
        # Internal drag: move the item and synchronize the file order.
        if event.source() is self:
            super().dropEvent(event)

            parent = self.parentWidget()

            if isinstance(parent, MergeWidget):
                parent.sync_pdf_files()

            return

        # External files: only PDF files are added.
        if event.mimeData().hasUrls():
            parent = self.parentWidget()

            if isinstance(parent, MergeWidget):
                parent.add_dropped_files(event.mimeData().urls())

            event.acceptProposedAction()
            return

        event.ignore()


class MergeWidget(QWidget):
    def __init__(
        self,
        language_manager: LanguageManager | None = None,
    ):
        super().__init__()

        # Use the shared language manager or English for standalone tests.
        self.language = language_manager or LanguageManager("en")

        self.pdf_files: list[Path] = []
        self.output_file: Path | None = None

        self.setup_ui()

    def clear_all(self):
        self.pdf_files.clear()
        self.file_list.clear()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel(
            self.language.get("merge.title")
        )
        layout.addWidget(self.title_label)

        self.file_list = PdfListWidget(self)
        layout.addWidget(self.file_list)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton(
            self.language.get("merge.add_pdf")
        )
        self.add_button.clicked.connect(self.add_pdf)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton(
            self.language.get("merge.remove_selected")
        )
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)

        self.clear_button = QPushButton(
            self.language.get("merge.clear_all")
        )
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)

        self.up_button = QPushButton(
            self.language.get("merge.move_up")
        )
        self.up_button.clicked.connect(self.move_up)
        button_layout.addWidget(self.up_button)

        self.down_button = QPushButton(
            self.language.get("merge.move_down")
        )
        self.down_button.clicked.connect(self.move_down)
        button_layout.addWidget(self.down_button)

        layout.addLayout(button_layout)

        output_layout = QHBoxLayout()

        self.output_label = QLabel(
            self.language.get("merge.output_not_selected")
        )
        output_layout.addWidget(self.output_label)

        self.output_button = QPushButton(
            self.language.get("merge.choose_output")
        )
        self.output_button.clicked.connect(self.choose_output)
        output_layout.addWidget(self.output_button)

        layout.addLayout(output_layout)

        self.merge_button = QPushButton(
            self.language.get("merge.merge_pdf")
        )
        self.merge_button.clicked.connect(self.merge_files)
        layout.addWidget(self.merge_button)

        self.setLayout(layout)

    def add_pdf(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            self.language.get("merge.choose_pdf"),
            "",
            "PDF Files (*.pdf)",
        )

        self.add_pdf_files(files)

    def add_pdf_files(self, files: list[str]):

        for file in files:
            path = Path(file)

            if path.suffix.lower() != ".pdf":
                continue

            if path not in self.pdf_files:
                self.pdf_files.append(path)
                self.add_list_item(path)

    def add_dropped_files(self, urls):

        files = []

        for url in urls:
            if not url.isLocalFile():
                continue

            path = Path(url.toLocalFile())

            if path.suffix.lower() == ".pdf":
                files.append(str(path))

        self.add_pdf_files(files)

    def sync_pdf_files(self):

        self.pdf_files = [
            Path(
                self.file_list.item(index).data(
                    Qt.ItemDataRole.UserRole
                )
            )
            for index in range(self.file_list.count())
        ]

    def add_list_item(self, path: Path):

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
            self.language.get("merge.choose_output"),
            "",
            "PDF Files (*.pdf)",
        )

        if not file:
            return

        self.output_file = Path(file)

        # Keep the output path visible for both users and tests.
        self.output_label.setText(
            f"{self.language.get('merge.output_prefix')}: "
            f"{self.output_file}"
        )

    def merge_files(self):

        if not self.pdf_files:
            QMessageBox.warning(
                self,
                self.language.get("merge.no_pdf_title"),
                self.language.get("merge.no_pdf_files"),
            )
            return

        if self.output_file is None:
            QMessageBox.warning(
                self,
                self.language.get("merge.no_output_title"),
                self.language.get("merge.no_output"),
            )
            return

        try:
            # Reuse the existing PDF processing logic.
            merge_pdfs(self.pdf_files, self.output_file)

        except Exception as exc:
            QMessageBox.critical(
                self,
                self.language.get("merge.failed"),
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            self.language.get("common.success"),
            self.language.get("merge.success"),
        )

    def refresh_ui(self):

        self.title_label.setText(
            self.language.get("merge.title")
        )

        self.add_button.setText(
            self.language.get("merge.add_pdf")
        )

        self.remove_button.setText(
            self.language.get("merge.remove_selected")
        )

        self.clear_button.setText(
            self.language.get("merge.clear_all")
        )

        self.up_button.setText(
            self.language.get("merge.move_up")
        )

        self.down_button.setText(
            self.language.get("merge.move_down")
        )

        self.output_button.setText(
            self.language.get("merge.choose_output")
        )

        self.merge_button.setText(
            self.language.get("merge.merge_pdf")
        )

        if self.output_file is None:
            self.output_label.setText(
                self.language.get("merge.output_not_selected")
            )
        else:
            self.output_label.setText(
                f"{self.language.get('merge.output_prefix')}: "
                f"{self.output_file}"
            )