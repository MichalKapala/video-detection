from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QLabel, \
    QSizePolicy, QCheckBox, QFrame, QLineEdit, QMessageBox, QComboBox, QAbstractItemView

from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
import cv2
import VideoProcessor.VideoProcessor as vp
from Utils.Statistics import FrameStatistics, VideoStatistics
import os


class VideoPlayer(QWidget):
    image_updated = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.play_icon = QIcon(r"View/Icons/play.png")
        self.pause_icon = QIcon(r"View/Icons/pause.png")

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
        self.processing_button = QCheckBox("Enable detections")
        self.processing_button.setChecked(True)
        self.processing_button.clicked.connect(self.toggle_processing)
        self.confidence_slider = QSlider(Qt.Orientation.Horizontal)
        self.confidence_label = QLabel("Confidence %")
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(50)
        self.confidence_slider.setSingleStep(5)
        self.confidence_slider.sliderReleased.connect(self.update_detector)
        self.confidence_label.setText("Confidence: {}%".format(self.confidence_slider.value()))

        self.class_combo_grid = QGridLayout()
        self.person_check = QCheckBox("Person")
        self.car_check = QCheckBox("Car")
        self.dog_check = QCheckBox("Dog")
        self.cat_check = QCheckBox("Cat")
        self.person_check.setChecked(True)
        self.car_check.setChecked(False)
        self.dog_check.setChecked(False)
        self.cat_check.setChecked(False)
        self.person_check.clicked.connect(self.update_detector)
        self.car_check.clicked.connect(self.update_detector)
        self.dog_check.clicked.connect(self.update_detector)
        self.cat_check.clicked.connect(self.update_detector)
        self.class_combo_grid.addWidget(self.person_check, 0, 0)
        self.class_combo_grid.addWidget(self.car_check, 0, 1)
        self.class_combo_grid.addWidget(self.dog_check, 1, 0)
        self.class_combo_grid.addWidget(self.cat_check, 1, 1)

        self.frame_settings_layout.addWidget(self.frame_settings_label)
        self.frame_settings_layout.addWidget(self.confidence_label)
        self.frame_settings_layout.addWidget(self.confidence_slider)
        self.frame_settings_layout.addLayout(self.class_combo_grid)
        self.frame_settings_layout.addWidget(self.processing_button)

        self.video_info_frame = QFrame()
        self.video_info_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.video_info_layout = QVBoxLayout(self.video_info_frame)

        self.video_info_label = QLabel("Video info")
        self.video_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_info_length_s = QLabel("Total wideo length: [s]")
        self.video_info_resolution = QLabel("Resolution: [px]")
        self.video_info_fps = QLabel("FPS: [fps]")

        self.video_info_layout.addWidget(self.video_info_label)
        self.video_info_layout.addWidget(self.video_info_length_s)
        self.video_info_layout.addWidget(self.video_info_resolution)
        self.video_info_layout.addWidget(self.video_info_fps)

        self.frame_info_frame = QFrame()
        self.frame_info_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.frame_info_layout = QVBoxLayout(self.frame_info_frame)

        self.frame_info_label = QLabel("Frame info")
        self.frame_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.frame_info_progress_label = QLabel("Processed frames")
        self.frame_info_count_label = QLabel("Number of detections: ")

        self.frame_info_layout.addWidget(self.frame_info_label)
        self.frame_info_layout.addWidget(self.frame_info_progress_label)
        self.frame_info_layout.addWidget(self.frame_info_count_label)

        self.save_video_frame = QFrame()
        self.save_video_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.save_video_layout = QVBoxLayout(self.save_video_frame)

        self.save_video_label = QLabel("Save")
        self.save_video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_check_box_layout = QHBoxLayout()
        self.save_detections_check_box = QCheckBox("Save detections")
        self.save_detections_check_box.setChecked(True)
        self.merge_detections_check_box = QCheckBox("Save video with detections")
        self.merge_detections_check_box.setChecked(True)
        self.save_video_button = QPushButton("Save")
        self.save_video_button.clicked.connect(self.save_video)

        self.save_video_layout.addWidget(self.save_video_label)
        self.save_video_layout.addWidget(self.save_detections_check_box)
        self.save_video_layout.addWidget(self.merge_detections_check_box)
        self.save_video_layout.addWidget(self.save_video_button)

        self.button_layout.addWidget(self.load_video_frame)
        self.button_layout.addWidget(self.frame_settings_frame)
        self.button_layout.addWidget(self.video_info_frame)
        self.button_layout.addWidget(self.frame_info_frame)
        self.button_layout.addWidget(self.save_video_frame)
        self.side_panel.setLayout(self.button_layout)

        # Slider layout
        self.slider_layout = QHBoxLayout()
        self.play_button = QPushButton()
        self.play_button.setIcon(self.play_icon)
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

        self.file_name = None
        self.is_playing = False

    @pyqtSlot()
    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Załaduj wideo")
        self.file_name = os.path.basename(file_path)
        if file_path != '':
            self.load_video_input.setText(file_path)
            self.backend.load_video(file_path)
            self.is_playing = True

    @pyqtSlot()
    def play_pause_video(self):
        self.backend.play_pause_video()

        if self.is_playing:
            self.play_button.setIcon(self.play_icon)
            self.is_playing = False
        else:
            self.play_button.setIcon(self.pause_icon)
            self.is_playing = True

    @pyqtSlot()
    def toggle_processing(self):
        self.backend.toggle_processing()

    @pyqtSlot(object, int)
    def update_image(self, frame, ctr):
        self.display_image(frame)
        self.progress_slider.setValue(ctr)

    @pyqtSlot(int)
    def set_up_video(self, ctr):
        self.play_button.setIcon(self.pause_icon)
        self.progress_slider.setRange(0, ctr)

    @pyqtSlot(int)
    def move_position(self, position):
        self.backend.set_video_position(position)

    @pyqtSlot()
    def remaining_frames_prompt(self):
        answer = QMessageBox.question(self,
                                      "Not all frames processed",
                                      "Not all frames were processed. Do you want to parse remaining frames?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes:
            self.backend.parse_remaining_frames()

    @pyqtSlot()
    def update_detector(self):
        classes = []
        if self.person_check.isChecked():
            classes.append(0)

        if self.car_check.isChecked():
            classes.append(2)

        if self.cat_check.isChecked():
            classes.append(15)

        if self.dog_check.isChecked():
            classes.append(16)

        self.confidence_label.setText("Confidence: {}%".format(self.confidence_slider.value()))
        confidence = self.confidence_slider.value() / 100

        self.backend.update_detector(confidence, classes)

    @pyqtSlot(FrameStatistics)
    def update_statistics(self, statistics):
        self.frame_info_progress_label.setText("Processed {}/{} frames".format(statistics.noOfProcessedFrames, statistics.totalFrames))
        self.frame_info_count_label.setText("Number of detections: {}".format(statistics.detectionCount))

    @pyqtSlot(VideoStatistics)
    def update_video_statistics(self, statistics):
        self.video_info_length_s.setText("Total wideo length: {} [s]".format(statistics.length_in_s))
        self.video_info_resolution.setText("Resolution: {}x{} [px]".format(statistics.frame_width, statistics.frame_height))
        self.video_info_fps.setText("FPS: {:.2f} [fps]".format(statistics.fps))

    @pyqtSlot()
    def restart_video(self):
        self.play_button.setIcon(self.play_icon)
        self.progress_slider.setValue(0)
        self.move_position(0)
        self.is_playing = False

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def save_video(self):
        directory_dialog = QFileDialog()
        path = directory_dialog.getExistingDirectory(self, "Wybierz folder do zapisu")

        if path != '':
            video_name = os.path.splitext(self.file_name)[0]
            video_filename = os.path.join(path, video_name + ".avi")
            self.backend.save_video(video_filename, self.merge_detections_check_box.isChecked())

            if self.save_detections_check_box.isChecked():
                detections_filename = os.path.join(path, video_name + ".json")
                self.backend.save_detections(detections_filename)