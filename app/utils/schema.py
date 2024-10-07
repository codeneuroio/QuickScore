from dataclasses import dataclass


@dataclass
class Event:
    idx: int
    frame: int
    time: float
    original_time: float
    is_discarded: bool = False
    is_flagged: bool = False
