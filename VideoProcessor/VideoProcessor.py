import cv2
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot
from FrameProcessor.FrameProcessor import FrameProcessor
from FrameProcessor.YoloHumanDetector import YoloHumanDetector
from VideoProcessor.DetectionStorage import DetectionStorage
from VideoProcessor.FrameStorage import FrameStorage
from VideoProcessor.VideoSaver import VideoSaver
from VideoProcessor.DetectionSaver import DetectionSaver
from Utils.Detection import Detection
from Utils.Statistics import FrameStatistics
import copy


def fill_detections_id(detections: list[Detection], id):
    for detection in detections:
        detection.id = id


class VideoProcessor(QObject):
    frame_processed = pyqtSignal(object, int)
    video_loaded = pyqtSignal(int)
    remaining_frames_prompt = pyqtSignal()
    send_statistics = pyqtSignal(FrameStatistics)

    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.processing_enabled = True
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.load_frame)
        self.frame_processor = FrameProcessor(YoloHumanDetector(0.5, [0]))
        self.detection_storage = DetectionStorage()
        self.orig_frame_storage = FrameStorage()
        self.processed_frame_storage = FrameStorage()
        self.video_saver = VideoSaver()
        self.detection_saver = DetectionSaver()

    def reset(self):
        self.processed_frame_storage.clear()
        self.orig_frame_storage.clear()
        self.detection_storage.clear()

    def load_video(self, file_name):
        if file_name != '':
            self.video_capture = cv2.VideoCapture(file_name)

            if not self.video_capture.isOpened():
                raise Exception(f"Błąd podczas otwierania pliku wideo: {file_name}")

            self.frame_timer.start(int(1000 / self.video_capture.get(cv2.CAP_PROP_FPS)))

            frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_loaded.emit(frame_count)

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

        if self.processing_enabled and ret:
            processed_frame, detections = self.frame_processor.process_frame(copy.copy(frame))
            self.frame_processed.emit(processed_frame, pos)
            if len(detections):
                fStatistices = FrameStatistics(len(detections), len(self.orig_frame_storage.frames), int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)))
                self.send_statistics.emit(fStatistices)
                fill_detections_id(detections, pos)
                self.detection_storage.add_detections(detections, pos)
        elif not self.processing_enabled and ret:
            self.frame_processed.emit(frame, pos)



    def set_video_position(self, position):
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, position)

    def save_video(self, file_name, merged):
        if len(self.orig_frame_storage.frames) != int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)):
            self.remaining_frames_prompt.emit()
        print(merged)
        if merged:
            self.video_saver.save_video_with_detections(self.orig_frame_storage.frames, self.detection_storage.detections, file_name)
        else:
            self.video_saver.save_video(self.orig_frame_storage.frames, file_name)

    def save_detections(self, file_name):
        self.detection_saver.save_detections(self.detection_storage.detections, file_name)

    def parse_remaining_frames(self):
        self.frame_timer.stop()
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 1)
        total_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        pos = 1

        while pos != total_count:
            pos = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            if pos not in self.orig_frame_storage.frames.keys():
                self.load_frame(pos)
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, pos + 1)

    def update_detector(self, confidence_threshold, classes):
        self.frame_processor = FrameProcessor(YoloHumanDetector(confidence_threshold, classes))


class Backend:
    def __init__(self):
        self.video_processor = VideoProcessor()

    def connect_signals(self, frontend):
        self.video_processor.frame_processed.connect(frontend.update_image)
        self.video_processor.video_loaded.connect(frontend.set_up_video)
        self.video_processor.remaining_frames_prompt.connect(frontend.remaining_frames_prompt)
        self.video_processor.send_statistics.connect(frontend.update_statistics)

    def load_video(self, file_name):
        self.video_processor.reset()
        self.video_processor.load_video(file_name)

    def play_pause_video(self):
        self.video_processor.play_pause_video()

    def toggle_processing(self):
        self.video_processor.toggle_processing()

    def set_video_position(self, position):
        self.video_processor.set_video_position(position)

    def save_video(self, file_name, merged):
        self.video_processor.save_video(file_name, merged)

    def save_detections(self, file_name):
        self.video_processor.save_detections(file_name)

    def parse_remaining_frames(self):
        self.video_processor.parse_remaining_frames()

    def update_detector(self, confidence, classes):
        self.video_processor.update_detector(confidence, classes)