import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl


class VideoPlayer(QMainWindow):
    """Class of VideoPlayer which plays a video chosen by user"""

    def __init__(self, file_path):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1024, 768)

        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile(file_path))

        self.video_widget = QVideoWidget()

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.play()

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
