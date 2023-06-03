from Utils.Detection import Detection
import cv2


class DetectionDrawer:
    def __init__(self):
        pass

    def draw_detections(self, frame, detections: list[Detection]):
        for detection in detections:
            self.draw_detection(frame, detection)

    def draw_detection(self, frame, detection: Detection):
        x, y, w, h = detection.coordinate
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
