from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from gui.delete_widget import DeleteWidget
from gui.merge_widget import MergeWidget
from gui.split_widget import SplitWidget
from gui.styles import APP_STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Toolkit")
        self.resize(900, 600)

        self.setStyleSheet(APP_STYLE)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        navigation_layout = QVBoxLayout()

        self.merge_button = QPushButton("Merge PDF")
        self.split_button = QPushButton("Split PDF")
        self.delete_button = QPushButton("Delete Pages")

        navigation_layout.addWidget(self.merge_button)
        navigation_layout.addWidget(self.split_button)
        navigation_layout.addWidget(self.delete_button)
        navigation_layout.addStretch()

        self.pages = QStackedWidget()

        # Keep each PDF operation as an independent widget.
        self.merge_widget = MergeWidget()
        self.split_widget = SplitWidget()
        self.delete_widget = DeleteWidget()

        self.pages.addWidget(self.merge_widget)
        self.pages.addWidget(self.split_widget)
        self.pages.addWidget(self.delete_widget)

        main_layout.addLayout(navigation_layout)
        main_layout.addWidget(self.pages)

        self.setCentralWidget(central_widget)

        self.setStatusBar(QStatusBar())

        # Connect navigation buttons to the corresponding pages.
        self.merge_button.clicked.connect(self.show_merge_page)
        self.split_button.clicked.connect(self.show_split_page)
        self.delete_button.clicked.connect(self.show_delete_page)

        self.show_merge_page()

    def show_merge_page(self):
        self.pages.setCurrentWidget(self.merge_widget)

    def show_split_page(self):
        self.pages.setCurrentWidget(self.split_widget)

    def show_delete_page(self):
        self.pages.setCurrentWidget(self.delete_widget)


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()