from PyQt6.QtWidgets import QApplication
from View.MainView import VideoPlayer

import qdarktheme

import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    main_window = VideoPlayer()
    main_window.resize(1200, 800)
    main_window.show()
    sys.exit(app.exec())