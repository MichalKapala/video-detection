from dataclasses import dataclass

@dataclass
class Coordinate:
    x: int
    y: int
    w: int
    h: int

@dataclass
class Detection:
    ID: int
    object_class: str
    confidence: float
    coordinate: Coordinate