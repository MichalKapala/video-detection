from Utils.Detection import Detection
from dataclasses import asdict
import json


class DetectionSaver:
    def __init__(self):
        pass

    def save_detections(self, detections, path):
        data_dict_list = []
        for detection_list in detections.values():
            data_dict_list += [asdict(obj) for obj in detection_list]

        with open(path, 'w') as file:
            json.dump(data_dict_list, file, indent=4)
