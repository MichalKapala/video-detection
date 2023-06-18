import cv2
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot
from FrameProcessor.FrameProcessor import FrameProcessor
from FrameProcessor.YoloHumanDetector import YoloHumanDetector
from VideoProcessor.DetectionStorage import DetectionStorage
from VideoProcessor.FrameStorage import FrameStorage
from VideoProcessor.VideoSaver import VideoSaver

class VideoProcessor(QObject):
    frame_processed = pyqtSignal(object, int)
    video_loaded = pyqtSignal(int)
    remaining_frames_prompt = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.processing_enabled = True
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.load_frame)
        self.frame_processor = FrameProcessor(YoloHumanDetector())
        self.detection_storage = DetectionStorage()
        self.orig_frame_storage = FrameStorage()
        self.processed_frame_storage = FrameStorage()
        self.video_saver = VideoSaver()

    def reset(self):
        self.processed_frame_storage.clear()
        self.orig_frame_storage.clear()
        self.detection_storage.clear()

    def load_video(self, file_name):
        if file_name != '':
            self.video_capture = cv2.VideoCapture(file_name)

            if not self.video_capture.isOpened():
                raise Exception(f"Błąd podczas otwierania pliku wideo: {file_name}")

            self.frame_timer.start(30)
            frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_loaded.emit(frame_count)

    def save_video(self, file_name):
        self.video_saver.save_video(self.frame_storage.frames, file_name)

    def play_pause_video(self):
        if self.frame_timer.isActive():
            self.frame_timer.stop()
        else:
            self.frame_timer.start(30)

    def toggle_processing(self):
        self.processing_enabled = not self.processing_enabled

    def load_frame(self, index=None):

        if self.video_capture is None or not self.video_capture.isOpened():
            return

        if index is not None:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, index)

        ret, frame = self.video_capture.read()
        pos = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
        self.orig_frame_storage.add_frame(frame, pos)

        if self.processing_enabled:
            frame, detections = self.frame_processor.process_frame(frame)
            self.detection_storage.add_detections(detections, pos)

        if ret:
            self.frame_processed.emit(frame, pos)
            self.processed_frame_storage.add_frame(frame, pos)

    def set_video_position(self, position):
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, position)

    def save_video(self, file_name):
        if len(self.orig_frame_storage.frames) != int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)):
            self.remaining_frames_prompt.emit()

        self.video_saver.save_video(self.processed_frame_storage.frames, file_name)

    def parse_remaining_frames(self):
        self.frame_timer.stop()
        self.frame_timer.start()
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 1)
        pos =1

        while pos != int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)):
            pos = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            if pos not in self.orig_frame_storage.frames.keys():
                self.load_frame(pos)
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, pos + 1)





class Backend:
    def __init__(self):
        self.video_processor = VideoProcessor()

    def connect_signals(self, frontend):
        self.video_processor.frame_processed.connect(frontend.update_image)
        self.video_processor.video_loaded.connect(frontend.set_up_video)
        self.video_processor.remaining_frames_prompt.connect(frontend.remaining_frames_prompt)

    def load_video(self, file_name):
        self.video_processor.reset()
        self.video_processor.load_video(file_name)

    def play_pause_video(self):
        self.video_processor.play_pause_video()

    def toggle_processing(self):
        self.video_processor.toggle_processing()

    def set_video_position(self, position):
        self.video_processor.set_video_position(position)

    def save_video(self, file_name):
        self.video_processor.save_video(file_name)

    def parse_remaining_frames(self):
        self.video_processor.parse_remaining_frames()