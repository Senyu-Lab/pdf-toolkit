from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.database.database import Database
from app.database.repository import HistoryRepository
from gui.delete_widget import DeleteWidget
from gui.i18n import LanguageManager
from gui.merge_widget import MergeWidget
from gui.settings import AppSettings
from gui.split_widget import SplitWidget
from gui.history_widget import HistoryWidget
from gui.styles import APP_STYLE


class MainWindow(QMainWindow):
    def __init__(
            self,
            settings: AppSettings | None = None,
    ):
        super().__init__()

        self.resize(900, 600)

        self.setStyleSheet(APP_STYLE)

        self.settings = settings or AppSettings()

        self.database = Database()
        self.history_repository = HistoryRepository(
            self.database,
        )

        language = self.settings.get_language()
        self.language = LanguageManager(language)

        # Refresh the UI whenever the language changes.
        self.language.language_changed.connect(self.refresh_ui)

        self.setup_ui()
        self.restore_window_state()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        navigation_layout = QVBoxLayout()

        self.merge_button = QPushButton()
        self.split_button = QPushButton()
        self.delete_button = QPushButton()
        self.history_button = QPushButton()

        navigation_layout.addWidget(self.merge_button)
        navigation_layout.addWidget(self.split_button)
        navigation_layout.addWidget(self.delete_button)
        navigation_layout.addWidget(self.history_button)
        navigation_layout.addStretch()

        self.pages = QStackedWidget()
        self.pages.currentChanged.connect(
            self._on_page_changed
        )


        # Share the same language manager and history repository with every page.
        self.merge_widget = MergeWidget(
            self.language,
            self.history_repository,
        )
        self.split_widget = SplitWidget(
            self.language,
            self.history_repository,
        )
        self.delete_widget = DeleteWidget(
            self.language,
            self.history_repository,
        )

        self.history_widget = HistoryWidget(
            self.language,
            self.history_repository,
        )

        self.pages.addWidget(self.merge_widget)
        self.pages.addWidget(self.split_widget)
        self.pages.addWidget(self.delete_widget)
        self.pages.addWidget(self.history_widget)

        # Language selector.
        self.language_selector = QComboBox()

        self.language_selector.addItem("English", "en")
        self.language_selector.addItem("中文", "zh")
        self.language_selector.addItem("日本語", "ja")

        self.language_selector.currentIndexChanged.connect(
            self.change_language
        )

        index = self.language_selector.findData(
            self.language.language
        )

        if index >= 0:
            self.language_selector.setCurrentIndex(index)

        main_layout.addLayout(navigation_layout)
        main_layout.addWidget(self.pages)

        self.setCentralWidget(central_widget)

        # Put the language selector into the status bar.
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_bar.addPermanentWidget(
            self.language_selector
        )

        # Navigation buttons.
        self.merge_button.clicked.connect(
            self.show_merge_page
        )
        self.split_button.clicked.connect(
            self.show_split_page
        )
        self.delete_button.clicked.connect(
            self.show_delete_page
        )
        self.history_button.clicked.connect(
            self.show_history_page
        )


        self.refresh_ui()
        self.show_merge_page()

    def change_language(self, index: int):
        language = self.language_selector.itemData(index)

        if language is None:
            return

        self.language.set_language(language)
        self.settings.save_language(language)

    def refresh_ui(self, language: str | None = None):

        self.setWindowTitle(
            self.language.get("app.title")
        )

        self.merge_button.setText(
            self.language.get("navigation.merge")
        )

        self.split_button.setText(
            self.language.get("navigation.split")
        )

        self.delete_button.setText(
            self.language.get("navigation.delete")
        )

        self.history_button.setText(
            self.language.get("navigation.history")
        )

        # Refresh the individual pages.
        self.merge_widget.refresh_ui()
        self.split_widget.refresh_ui()
        self.delete_widget.refresh_ui()
        self.history_widget.refresh_ui()

    def show_merge_page(self):
        self.pages.setCurrentWidget(
            self.merge_widget
        )

    def show_split_page(self):
        self.pages.setCurrentWidget(
            self.split_widget
        )

    def show_delete_page(self):
        self.pages.setCurrentWidget(
            self.delete_widget
        )

    def show_history_page(self):
        self.pages.setCurrentWidget(
            self.history_widget
        )

    def restore_window_state(self):
        geometry = self.settings.get_window_geometry()

        if geometry is not None:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        self.settings.save_window_geometry(
            self.saveGeometry()
        )

        event.accept()

    def _on_page_changed(self, index: int):
        if self.pages.widget(index) is self.history_widget:
            self.history_widget.refresh_history()

def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()