import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import fileBrowser as fb


class GUI:
    """Main GUI window of the app"""

    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.resize(230, 80)
        self.window.move(100, 100)
        self.window.setWindowTitle("VideoDetect")
        self.window.show()
        self.layout = QVBoxLayout()
        self.fileBrowser = fb.FileBrowser()

        # gui elements
        self.addFileLabel = QLabel("Choose .avi file to load:")

        self.layout.addWidget(self.addFileLabel)
        self.layout.addWidget(self.fileBrowser)
        self.window.setLayout(self.layout)

        sys.exit(self.app.exec())
