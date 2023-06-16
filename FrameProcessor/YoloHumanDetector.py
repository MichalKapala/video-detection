from Utils.Detection import Detection
from Utils.Detection import Coordinate
import numpy as np
import cv2
import torch


def unwrap_detection(input_image, output_data):
    pass

class YoloHumanDetector:
    def __init__(self):
        self.net  = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.net.conf = 0.4
        self.net.iou = 0.5
        self.net.classes = [0]

    def get_detections(self, frame) -> list[Detection]:
        detections = []

        outputs = self.net(frame)

        for output in outputs.pandas().xyxy[0].to_numpy():
            detections.append(Detection(Coordinate(output[0], output[1], output[2] - output[0], output[3] - output[1]), 0, 0))

        return detections
