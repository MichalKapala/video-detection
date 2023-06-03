from FrameProcessor.HumanDetector import HumanDetector
import cv2


class HogHumanDetector(HumanDetector):
    def __init__(self):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        super().__init__(hog)
