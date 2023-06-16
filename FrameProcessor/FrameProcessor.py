import FrameProcessor.DetectionDrawer as dd


class FrameProcessor:
    def __init__(self, detector):
        self.detector = detector

    def process_frame(self, frame):
        detections = self.detector.get_detections(frame)
        dd.draw_detections(frame, detections)
        return frame, detections
