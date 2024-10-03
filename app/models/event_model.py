import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal


class EventModel(QObject):
    events_loaded = pyqtSignal()
    current_event_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.events_path = ""
        self.events = []
        self.n_events = 0
        self._event_id = 0

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, value):
        if 0 <= value < self.n_events:
            self._event_id = value
            self.current_event_changed.emit(self.events[value])

    def load_events(self, path):
        self.events_path = path
        with open(self.events_path, "r", encoding="utf-8-sig") as f:
            self.events = np.genfromtxt(f, dtype=float, delimiter=",")
            self.n_events = len(self.events)
        self.events_loaded.emit()
