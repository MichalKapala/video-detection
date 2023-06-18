from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QLabel, \
    QSizePolicy, QCheckBox, QFrame, QLineEdit

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

        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.sliderMoved.connect(self.move_position)

        self.side_panel = QWidget()
        self.side_panel.setFixedWidth(400)
        self.button_layout = QVBoxLayout()

        self.load_video_frame = QFrame()
        self.load_video_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.load_video_layout = QVBoxLayout(self.load_video_frame)

        self.load_video_label = QLabel("Load video")
        self.load_video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_video_input = QLineEdit()
        self.load_video_input.setEnabled(False)
        self.load_button = QPushButton("Load video")
        self.load_button.clicked.connect(self.load_video)

        self.load_video_layout.addWidget(self.load_video_label)
        self.load_video_layout.addWidget(self.load_video_input)
        self.load_video_layout.addWidget(self.load_button)

        self.frame_settings_frame = QFrame()
        self.frame_settings_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.frame_settings_layout = QVBoxLayout(self.frame_settings_frame)

        self.frame_settings_label = QLabel("Settings")
        self.frame_settings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processing_button = QCheckBox("Włącz detekcję")
        self.processing_button.setChecked(True)
        self.processing_button.clicked.connect(self.toggle_processing)

        self.frame_settings_layout.addWidget(self.frame_settings_label)
        self.frame_settings_layout.addWidget(self.processing_button)

        self.video_info_frame = QFrame()
        self.video_info_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.video_info_layout = QVBoxLayout(self.video_info_frame)

        self.video_info_label = QLabel("Video info")
        self.video_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_info_layout.addWidget(self.video_info_label)

        self.frame_info_frame = QFrame()
        self.frame_info_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.frame_info_layout = QVBoxLayout(self.frame_info_frame)

        self.frame_info_label = QLabel("Frame info")
        self.frame_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.frame_info_layout.addWidget(self.frame_info_label)

        self.save_video_frame = QFrame()
        self.save_video_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.save_video_layout = QVBoxLayout(self.save_video_frame)

        self.save_video_label = QLabel("Save")
        self.save_video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_video_button = QPushButton("Save video")
        self.save_video_button.clicked.connect(self.save_video)
        self.save_detection_button = QPushButton("Save detections")
        # self.save_detection_button.clicked.connect(self.save_detection)

        self.save_video_layout.addWidget(self.save_video_label)
        self.save_video_layout.addWidget(self.save_video_button)
        self.save_video_layout.addWidget(self.save_detection_button)

        self.button_layout.addWidget(self.load_video_frame)
        self.button_layout.addWidget(self.frame_settings_frame)
        self.button_layout.addWidget(self.video_info_frame)
        self.button_layout.addWidget(self.frame_info_frame)
        self.button_layout.addWidget(self.save_video_frame)
        self.side_panel.setLayout(self.button_layout)

        # Slider layout
        self.slider_layout = QHBoxLayout()
        self.play_button = QPushButton("Zatrzymaj")
        self.play_button.clicked.connect(self.play_pause_video)
        self.slider_layout.addWidget(self.play_button)
        self.slider_layout.addWidget(self.progress_slider)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.image_label, 0, 0, 1, 2)
        self.layout.addWidget(self.side_panel, 0, 2)
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
