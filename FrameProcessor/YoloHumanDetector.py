from Utils.Detection import Detection
from Utils.Detection import Coordinate
import numpy as np
import cv2
import torch

object_class_map  = { 0 : "person", 2 : "car", 15: "cat", 16: "dog" }

class YoloHumanDetector:
    def __init__(self, confidence, classes):
        self.net  = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.net.conf = confidence
        self.net.classes = classes
        self.net.iou = 0.5

    def get_detections(self, frame) -> list[Detection]:
        detections = []

        outputs = self.net(frame)

        for output in outputs.pandas().xyxy[0].to_numpy():
            detections.append(Detection(0, object_class_map[output[5]], output[4], Coordinate(output[0], output[1], output[2] - output[0], output[3] - output[1])))

        return detections
