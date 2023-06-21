import cv2
import FrameProcessor.DetectionDrawer as dd
class VideoSaver:
    def __init__(self):
        self.fps = 30

    def save_video(self, frames, output_file_name):
        if len(frames) == 0:
            return

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file_name, fourcc, self.fps, (frames[1].shape[1], frames[1].shape[0]))
        for frame in frames.values():
            out.write(frame)

        out.release()

    def save_video_with_detections(self, frames, detections, output_file_name):
        if len(frames) == 0:
            return

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file_name, fourcc, self.fps, (frames[1].shape[1], frames[1].shape[0]))
        for frame_id in frames.keys():
            frame = frames[frame_id]
            if frame_id in detections.keys():
                for detection in detections[frame_id]:
                    dd.draw_detection(frame, detection)
                out.write(frame)

        out.release()