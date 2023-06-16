import os

from PyQt6.QtWidgets import QWidget, QPushButton, QFileDialog, QMessageBox
import View.videoPlayer as vp


class FileBrowser(QWidget):
    """Class of FileBrowser, which can be used to choose .avi file to be played in
    the new window"""

    def __init__(self):
        super().__init__()

        self.videoPlayer = None
        # Create a button to open the file dialog
        self.button = QPushButton('Open File', self)
        self.button.clicked.connect(self.showFileDialog)

    def showFileDialog(self):
        # Open a file dialog and get the selected file path
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open file', '', 'AVI Files (*.avi)')

        max_file_size = 100000000  # 100 MB
        file_size = os.path.getsize(file_path)

        if file_size > max_file_size:
            # Display an error message if the file size is too large
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Icon.Critical)
            message_box.setWindowTitle('Error')
            message_box.setText('The selected file is too large.')
            message_box.exec()
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.setWindowTitle('Success')
            message_box.setText('The selected file is loaded and will be opened in the new window.')
            message_box.exec()

            self.videoPlayer = vp.VideoPlayer(file_path)

            self.videoPlayer.show()
