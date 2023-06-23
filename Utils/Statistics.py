from dataclasses import dataclass


@dataclass
class FrameStatistics:
    detectionCount: int
    noOfProcessedFrames: int
    totalFrames: int

@dataclass
class VideoStatistics:
    length_in_s: int
    frame_width: int
    frame_height: int
    fps: float

