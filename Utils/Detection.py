from dataclasses import dataclass

@dataclass
class Coordinate:
    x: int
    y: int
    w: int
    h: int

@dataclass
class Detection:
    coordinate: Coordinate
    timestamp: float
    frame_number: int