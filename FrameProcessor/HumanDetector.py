from Utils.Detection import Detection


class HumanDetector:
    def __init__(self, detector):
        self.detector = detector

    def get_detections(self, frame) -> list[Detection]:
        detections = []
        boxes, _ = self.detector.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

        for (x, y, w, h) in boxes:
            det = Detection((x, y, w, h), 0, 0)
            detections.append(det)

        return detections
