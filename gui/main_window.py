from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from gui.delete_widget import DeleteWidget
from gui.merge_widget import MergeWidget
from gui.split_widget import SplitWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Toolkit")
        self.resize(800, 500)

        tabs = QTabWidget()

        tabs.addTab(MergeWidget(), "Merge PDF")
        tabs.addTab(SplitWidget(), "Split PDF")
        tabs.addTab(DeleteWidget(), "Delete Pages")

        self.setCentralWidget(tabs)


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()