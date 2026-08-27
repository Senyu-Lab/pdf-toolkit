from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
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

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.history_table)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

        self.refresh_ui()

    def refresh_history(self):
        if self.history_repository is None:
            self.history_table.setRowCount(0)
            return

        operations = self.history_repository.get_operations()

        self.history_table.setRowCount(len(operations))

        for row, operation in enumerate(operations):
            self.history_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    operation["created_at"]
                ),
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