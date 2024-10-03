import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal


class EventModel(QObject):
    events_loaded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.events_path = ""
        self.events = []
        self.event_id = 0

    def load_events(self, path):
        self.events_path = path
        with open(self.events_path, "r", encoding="utf-8-sig") as f:
            self.events = np.genfromtxt(f, dtype=float, delimiter=",")
        self.events_loaded.emit()
