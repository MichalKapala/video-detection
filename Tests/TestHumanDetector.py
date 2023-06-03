import unittest
from FrameProcessor.HogHumanDetector import HogHumanDetector
import cv2


class TestHumanDetector(unittest.TestCase):

    def test_detection_presence(self):
        img = cv2.imread("resources/test_img_1.jpg")
        img = cv2.resize(img, (800, 800))
        detector = HogHumanDetector()
        detections = detector.get_detections(img)
        self.assertGreater(len(detections), 0)


if __name__ == '__main__':
    unittest.main()
