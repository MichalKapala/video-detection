import cv2
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot
from FrameProcessor.FrameProcessor import FrameProcessor
from FrameProcessor.YoloHumanDetector import YoloHumanDetector

class VideoProcessor(QObject):
    frame_processed = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.processing_enabled = True
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.load_frame)
        self.frame_processor = FrameProcessor(YoloHumanDetector())

    def load_video(self, file_name):
        if file_name != '':
            self.video_capture = cv2.VideoCapture(file_name)

            if not self.video_capture.isOpened():
                raise Exception(f"Błąd podczas otwierania pliku wideo: {file_name}")

            frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.frame_processed.emit(frame_count)
            self.frame_timer.start(30)

    def play_pause_video(self):
        if self.frame_timer.isActive():
            self.frame_timer.stop()
        else:
            self.frame_timer.start(30)

    def toggle_processing(self):
        self.processing_enabled = not self.processing_enabled

    def load_frame(self):
        if self.video_capture is None or not self.video_capture.isOpened():
            return
        ret, frame = self.video_capture.read()

        if self.processing_enabled:
            frame, detections = self.frame_processor.process_frame(frame)

        if ret:
            self.frame_processed.emit(frame)


class Backend:
    def __init__(self):
        self.video_processor = VideoProcessor()

    def connect_signals(self, frontend):
        self.video_processor.frame_processed.connect(frontend.update_image)

    def load_video(self, file_name):
        self.video_processor.load_video(file_name)

    def play_pause_video(self):
        self.video_processor.play_pause_video()

    def toggle_processing(self):
        self.video_processor.toggle_processing()