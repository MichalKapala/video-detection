from Utils.Detection import Detection
import cv2

class_type_color_map = {
    "person": (0, 255, 0),
    "car": (0, 0, 255),
    "cat": (255, 0, 0),
    "dog": (255, 255, 0)
}

def draw_detection(frame, detection: Detection):
    x,y, w, h = int(detection.coordinate.x), int(detection.coordinate.y), int(detection.coordinate.w), int(detection.coordinate.h)
    cv2.rectangle(frame, (x, y), (x + w, y + h), class_type_color_map[detection.object_class], 2)
    cv2.putText(frame, detection.object_class, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, class_type_color_map[detection.object_class], 2)


def draw_detections(frame, detections: list[Detection]):
    for detection in detections:
        draw_detection(frame, detection)
