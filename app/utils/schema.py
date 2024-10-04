from dataclasses import dataclass


@dataclass
class Event:
    idx: int
    frame: int
    time: float
    original_time: float
    deleted: bool = False
    flagged: bool = False
