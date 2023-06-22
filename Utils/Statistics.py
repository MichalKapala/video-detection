from dataclasses import dataclass


@dataclass
class FrameStatistics:
    detectionCount: int
    noOfProcessedFrames: int
    totalFrames: int

