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

from gui.delete_widget import DeleteWidget
from gui.i18n import LanguageManager
from gui.merge_widget import MergeWidget
from gui.split_widget import SplitWidget
from gui.styles import APP_STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(900, 600)

        self.setStyleSheet(APP_STYLE)

        # Use one language manager for the entire GUI.
        self.language = LanguageManager("en")

        # Refresh the UI whenever the language changes.
        self.language.language_changed.connect(self.refresh_ui)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        navigation_layout = QVBoxLayout()

        self.merge_button = QPushButton()
        self.split_button = QPushButton()
        self.delete_button = QPushButton()

        navigation_layout.addWidget(self.merge_button)
        navigation_layout.addWidget(self.split_button)
        navigation_layout.addWidget(self.delete_button)
        navigation_layout.addStretch()

        self.pages = QStackedWidget()

        # Share the same language manager with every page.
        self.merge_widget = MergeWidget(self.language)
        self.split_widget = SplitWidget(self.language)
        self.delete_widget = DeleteWidget(self.language)

        self.pages.addWidget(self.merge_widget)
        self.pages.addWidget(self.split_widget)
        self.pages.addWidget(self.delete_widget)

        # Language selector.
        self.language_selector = QComboBox()

        self.language_selector.addItem("English", "en")
        self.language_selector.addItem("中文", "zh")
        self.language_selector.addItem("日本語", "ja")

        self.language_selector.currentIndexChanged.connect(
            self.change_language
        )

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

        self.refresh_ui()
        self.show_merge_page()

    def change_language(self, index: int):
        """Change the application language."""

        language = self.language_selector.itemData(index)

        if language is None:
            return

        self.language.set_language(language)

    def refresh_ui(self, language: str | None = None):
        """Refresh all visible application text."""

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

        # Refresh the individual pages.
        self.merge_widget.refresh_ui()
        self.split_widget.refresh_ui()
        self.delete_widget.refresh_ui()

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


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()