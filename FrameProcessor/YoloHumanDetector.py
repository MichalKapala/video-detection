from Utils.Detection import Detection
import cv2


class YoloHumanDetector:
    def __init__(self):
        self.net = cv2.dnn.readNet("../Models/yolov5s.onnx")
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

    def get_detections(self, frame) -> list[Detection]:
        detections = []
        self.prepare_frame(frame)

    def prepare_frame(self, frame):
        print(frame.shape)