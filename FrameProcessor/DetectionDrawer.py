from Utils.Detection import Detection
import cv2


def draw_detection(frame, detection: Detection):
    x,y, w, h = int(detection.coordinate.x), int(detection.coordinate.y), int(detection.coordinate.w), int(detection.coordinate.h)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


def draw_detections(frame, detections: list[Detection]):
    for detection in detections:
        draw_detection(frame, detection)
