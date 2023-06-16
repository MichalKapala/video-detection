from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QLabel, \
    QSizePolicy, QCheckBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
import cv2
import VideoProcessor.VideoProcessor as vp


class VideoPlayer(QWidget):
    image_updated = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Frontend elements
        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.load_button = QPushButton("Załaduj wideo")
        self.load_button.clicked.connect(self.load_video)
        self.processing_button = QCheckBox("Włącz detekcję")
        self.processing_button.setChecked(True)
        self.processing_button.clicked.connect(self.toggle_processing)
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.sliderMoved.connect(self.move_position)
        self.save_video_button = QPushButton("Zapisz wideo")
        self.save_video_button.clicked.connect
        self.save_detection_button = QPushButton("Zapisz detekcję")
        # self.save_detection_button.clicked.connect(self.save_detection)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addWidget(self.processing_button)
        self.button_layout.addWidget(self.save_video_button)
        self.button_layout.addWidget(self.save_detection_button)

        # Slider layout
        self.slider_layout = QHBoxLayout()
        self.play_button = QPushButton("Zatrzymaj")
        self.play_button.clicked.connect(self.play_pause_video)
        self.slider_layout.addWidget(self.play_button)
        self.slider_layout.addWidget(self.progress_slider)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.image_label, 0, 0, 1, 2)
        self.layout.addLayout(self.button_layout, 0, 2)
        self.layout.addLayout(self.slider_layout, 1, 0, 1, 2)
        self.setLayout(self.layout)

        # Backend
        self.backend = vp.Backend()
        self.backend.connect_signals(self)

    @pyqtSlot()
    def load_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Załaduj wideo")
        if file_name != '':
            self.backend.load_video(file_name)

    @pyqtSlot()
    def play_pause_video(self):
        self.backend.play_pause_video()

    @pyqtSlot()
    def toggle_processing(self):
        self.backend.toggle_processing()

    @pyqtSlot(object, int)
    def update_image(self, frame, ctr):
        self.display_image(frame)
        self.progress_slider.setValue(ctr)

    @pyqtSlot(int)
    def set_up_video(self, ctr):
        self.progress_slider.setRange(0, ctr)

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    @pyqtSlot(int)
    def move_position(self, position):
        self.backend.set_video_position(position)

    def save_video(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz wideo")
        if file_name != '':
            self.backend.save_video(file_name)
