import cv2
from Utils.Detection import Detection


class HogHumanDetector:
    def __init__(self):
        self.detector = cv2.HOGDescriptor()
        self.detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def get_detections(self, frame) -> list[Detection]:
        detections = []
        boxes, _ = self.detector.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

        for (x, y, w, h) in boxes:
            det = Detection(0, "", 0, (x, y, w, h))
            detections.append(det)

        return detections
