import cv2
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