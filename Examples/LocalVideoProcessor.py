import FrameProcessor.FrameProcessor as fp
import FrameProcessor.HogHumanDetector as hhd
import FrameProcessor.YoloHumanDetector as yhd

import cv2


class LocalVideoProcessor:
    def __init__(self, video_path, frame_processor):
        self.video_path = video_path
        self.frame_processor = frame_processor

        self.frames = []
        self.detections = []

    def process_video(self):

        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                processed_frame, detections = self.frame_processor.process_frame(frame)
                self.frames.append(processed_frame)
                self.detections.append(detections)

                if len(self.frames) % 1000 == 0:
                    print("Processed {} frames".format(len(self.frames)))
            else:
                break
        cap.release()

    def has_frames(self):
        return len(self.frames) > 0

    def pop_frame(self):
        return self.frames.pop(0)


class VideoSaver:
    def __init__(self, out_path):
        self.video_path = out_path
        self.frames = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def save_video(self):
        height, width, layers = self.frames[0].shape
        size = (width, height)
        out = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

        for frame in self.frames:
            out.write(frame)
        out.release()


frameProcessor = fp.FrameProcessor(yhd.YoloHumanDetector())
processor = LocalVideoProcessor("/home/mkapala/Downloads/vid.avi", frameProcessor)
processor.process_video()

saver = VideoSaver("/home/mkapala/Downloads/vid_out.avi")

while processor.has_frames():
    frame = processor.pop_frame()
    saver.add_frame(frame)

saver.save_video()
