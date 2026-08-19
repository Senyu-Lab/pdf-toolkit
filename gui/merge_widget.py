from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.merger import merge_pdfs


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

        self.file_list = QListWidget()
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

        for file in files:
            path = Path(file)

            # Avoid adding the same PDF more than once.
            if path not in self.pdf_files:
                self.pdf_files.append(path)
                self.file_list.addItem(path.name)

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