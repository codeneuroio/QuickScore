from dataclasses import dataclass, field
import numpy as np
from utils.schema import Event
from typing import Optional


@dataclass
class PlaybackState:
    files_loaded: bool = False


@dataclass
class VideoState:
    loaded: bool = False
    path: str = ""
    fps: float = 0
    width: int = 0
    height: int = 0


@dataclass
class EventState:
    loaded: bool = False
    path: str = ""
    current_event: Optional[Event] = None


@dataclass
class TimeSeriesState:
    loaded: bool = False
    path: str = ""
    data: np.ndarray = np.array([])


@dataclass
class AppState:
    playback: PlaybackState = field(default_factory=PlaybackState)
    video: VideoState = field(default_factory=VideoState)
    event: EventState = field(default_factory=EventState)
    timeseries: TimeSeriesState = field(default_factory=TimeSeriesState)
