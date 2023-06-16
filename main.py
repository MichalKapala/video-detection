from PyQt6.QtWidgets import QApplication
from View.MainView import VideoPlayer

import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = VideoPlayer()
    main_window.resize(800, 600)
    main_window.show()
    sys.exit(app.exec())