import cv2
class VideoSaver:
    def __init__(self):
        self.frames = []
        self.fps = 30

    def save_video(self, frames, output_file_name):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file_name, fourcc, self.fps, (frames[0].shape[1], frames[0].shape[0]))
        for frame in frames:
            out.write(frame)

        out.release()