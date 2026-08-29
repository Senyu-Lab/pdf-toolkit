from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.database.repository import HistoryRepository
from gui.i18n import LanguageManager


class HistoryWidget(QWidget):
    def __init__(
        self,
        language_manager: LanguageManager | None = None,
        history_repository: HistoryRepository | None = None,
    ):
        super().__init__()

        # Use the shared language manager or English for standalone tests.
        self.language = language_manager or LanguageManager("en")
        self.history_repository = history_repository

        self.setup_ui()
        self.refresh_history()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.title_label = QLabel()
        self.title_label.setObjectName("pageTitle")

        self.description_label = QLabel()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)

        self.history_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.history_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.history_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.history_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.refresh_button = QPushButton()
        self.refresh_button.setObjectName("primaryButton")
        self.refresh_button.clicked.connect(
            self.refresh_history
        )

        self.delete_button = QPushButton()
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(
            self.delete_selected_operation
        )

        self.clear_button = QPushButton()
        self.clear_button.setObjectName("secondaryButton")
        self.clear_button.clicked.connect(
            self.clear_history
        )

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.history_table)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

        self.refresh_ui()

    def refresh_history(self):
        if self.history_repository is None:
            self.history_table.setRowCount(0)
            return

        operations = self.history_repository.get_operations()

        self.history_table.setRowCount(len(operations))

        for row, operation in enumerate(operations):
            time_item = QTableWidgetItem(
                operation["created_at"]
            )
            time_item.setData(
                Qt.ItemDataRole.UserRole,
                operation["id"],
            )
            self.history_table.setItem(
                row,
                0,
                time_item,
            )

            self.history_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    operation["operation_type"]
                ),
            )

            self.history_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    operation["status"]
                ),
            )

            self.history_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    ", ".join(operation["input_files"])
                ),
            )

            self.history_table.setItem(
                row,
                4,
                QTableWidgetItem(
                    ", ".join(operation["output_files"])
                ),
            )


    def delete_selected_operation(self):
        row = self.history_table.currentRow()

        if row < 0:
            return

        item = self.history_table.item(row, 0)

        if item is None:
            return

        operation_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if operation_id is None:
            return

        result = QMessageBox.question(
            self,
            self.language.get("history.delete_title"),
            self.language.get("history.delete_confirmation"),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if result != QMessageBox.StandardButton.Yes:
            return

        self.history_repository.delete_operation(
            operation_id
        )

        self.refresh_history()

    def clear_history(self):
        result = QMessageBox.question(
            self,
            self.language.get(
                "history.clear_title"
            ),
            self.language.get(
                "history.clear_confirmation"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if result != QMessageBox.StandardButton.Yes:
            return

        if self.history_repository is None:
            return

        self.history_repository.clear_operations()

        self.refresh_history()

    def refresh_ui(self):
        self.title_label.setText(
            self.language.get("history.title")
        )

        self.description_label.setText(
            self.language.get("history.description")
        )

        self.history_table.setHorizontalHeaderLabels(
            [
                self.language.get("history.time"),
                self.language.get("history.operation"),
                self.language.get("history.status"),
                self.language.get("history.input_files"),
                self.language.get("history.output_files"),
            ]
        )

        self.refresh_button.setText(
            self.language.get("history.refresh")
        )

        self.delete_button.setText(
            self.language.get("history.delete")
        )

        self.clear_button.setText(
            self.language.get("history.clear")
        )
