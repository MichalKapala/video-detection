## Class to storage frames in a dict
import sys
class FrameStorage:
    def __init__(self):
        self.frames = {}

    def add_frame(self, frame, frame_id):
        self.frames[frame_id] = frame

    def clear(self):
        self.frames = {}

    def get_frame(self, frame_id):
        return self.frames[frame_id]

    def has_frame(self, frame_id):
        return frame_id in self.frames.keys()