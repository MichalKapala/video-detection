import cv2
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QLabel, \
    QSizePolicy, QCheckBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from FrameProcessor.FrameProcessor import FrameProcessor
from FrameProcessor.YoloHumanDetector import YoloHumanDetector


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # frontend elements
        self.video_capture = None
        self.processing_enabled = True
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.load_frame)

        # Side panel layout
        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.load_button = QPushButton("Załaduj wideo")
        self.load_button.clicked.connect(self.load_video)
        self.processing_button = QCheckBox("Włącz detekcję")
        self.processing_button.setChecked(True)
        self.processing_button.clicked.connect(self.toggle_processing)
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 0)
        self.progress_slider.sliderMoved.connect(self.move_position)
        self.save_video_button = QPushButton("Zapisz wideo")
        # self.save_video_button.clicked.connect(self.save_video)
        self.save_detection_button = QPushButton("Zapisz detekcję")
        # self.save_detection_button.clicked.connect(self.save_detection)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addWidget(self.processing_button)
        self.button_layout.addWidget(self.save_video_button)
        self.button_layout.addWidget(self.save_detection_button)

        # slider layout
        self.slider_layout = QHBoxLayout()
        self.play_button = QPushButton("Zatrzymaj")
        self.play_button.clicked.connect(self.play_pause_video)
        self.slider_layout.addWidget(self.play_button)
        self.slider_layout.addWidget(self.play_button)
        self.slider_layout.addWidget(self.progress_slider)

        # layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.image_label, 0, 0, 1, 2)
        self.layout.addLayout(self.button_layout, 0, 2)
        self.layout.addLayout(self.slider_layout, 1, 0, 1, 2)
        self.setLayout(self.layout)

        # backend elements
        self.frame_processor = FrameProcessor(YoloHumanDetector())

    def load_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Załaduj wideo")
        if file_name != '':
            self.video_capture = cv2.VideoCapture(file_name)

            if not self.video_capture.isOpened():
                raise Exception(f"Błąd podczas otwierania pliku wideo: {file_name}")

            self.progress_slider.setRange(0, int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)))
            self.frame_timer.start(30)

    def play_pause_video(self):
        if self.frame_timer.isActive():
            self.frame_timer.stop()
            self.play_button.setText("Wznów")
        else:
            self.frame_timer.start(30)
            self.play_button.setText("Zatrzymaj")

    def toggle_processing(self):
        self.processing_enabled = not self.processing_enabled
        self.processing_button.setText("Włącz detekcję" if not self.processing_enabled else "Wyłącz detekcję")

    def load_frame(self):
        if self.video_capture is None or not self.video_capture.isOpened():
            return
        ret, frame = self.video_capture.read()

        if self.processing_enabled:
            frame, detections = self.frame_processor.process_frame(frame)
        if ret:
            self.display_image(frame)
            self.progress_slider.setValue(self.progress_slider.value() + 1)

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def move_position(self, position):
        if self.video_capture is not None:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, position)
