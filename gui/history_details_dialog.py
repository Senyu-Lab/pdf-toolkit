import json

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QListWidget,
    QVBoxLayout,
)

from gui.i18n import LanguageManager


class HistoryDetailsDialog(QDialog):
    def __init__(
        self,
        language: LanguageManager,
        operation: dict,
        parent=None,
    ):
        super().__init__(parent)

        self.language = language
        self.operation = operation

        self.setup_ui()

        self.refresh_ui()

    def setup_ui(self):
        self.resize(700, 400)
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.operation_label = QLabel()
        self.status_label = QLabel()
        self.created_at_label = QLabel()

        self.input_files_list = QListWidget()
        self.output_files_list = QListWidget()

        form_layout.addRow(
            self.language.get("history.operation"),
            self.operation_label,
        )

        form_layout.addRow(
            self.language.get("history.status"),
            self.status_label,
        )

        form_layout.addRow(
            self.language.get("history.created_at"),
            self.created_at_label,
        )

        form_layout.addRow(
            self.language.get("history.input_files"),
            self.input_files_list,
        )

        form_layout.addRow(
            self.language.get("history.output_files"),
            self.output_files_list,
        )

        self.error_label = QLabel()
        self.error_label.setWordWrap(True)

        form_layout.addRow(
            self.language.get("history.error"),
            self.error_label,
        )

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )

        self.button_box.rejected.connect(
            self.reject
        )

        layout.addWidget(self.button_box)

    def refresh_ui(self):
        self.setWindowTitle(
            self.language.get(
                "history.details_title"
            )
        )

        self.operation_label.setText(
            str(
                self.operation.get(
                    "operation_type",
                    "",
                )
            )
        )

        self.status_label.setText(
            str(
                self.operation.get(
                    "status",
                    "",
                )
            )
        )

        self.created_at_label.setText(
            str(
                self.operation.get(
                    "created_at",
                    "",
                )
            )
        )

        self._refresh_file_list(
            self.input_files_list,
            self.operation.get(
                "input_files",
                [],
            ),
        )

        self._refresh_file_list(
            self.output_files_list,
            self.operation.get(
                "output_files",
                [],
            ),
        )

        error_message = self.operation.get(
            "error_message"
        )

        self.error_label.setText(
            str(error_message)
            if error_message
            else "-"
        )

    def _refresh_file_list(
        self,
        widget: QListWidget,
        files,
    ):
        widget.clear()

        if isinstance(files, str):
            try:
                files = json.loads(files)
            except json.JSONDecodeError:
                files = [files]

        for file_path in files:
            widget.addItem(
                str(file_path)
            )