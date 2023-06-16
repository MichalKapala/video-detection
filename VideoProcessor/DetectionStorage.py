
class DetectionStorage:
    def __init__(self):
        self.detections = {}

    def add_detections(self, detections: list, frame_id):
        self.detections[frame_id] = detections

    def clear(self):
        self.detections = {}

    def get_detections(self, frame_id):
        return self.detections[frame_id]

    def has_detections(self, frame_id):
        return frame_id in self.detections.keys()

