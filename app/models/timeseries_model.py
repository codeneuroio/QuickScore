import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal


class TimeSeriesModel(QObject):
    timeseries_loaded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timeseries_path = ""
        self.timeseries = None

    def load_timeseries(self, path):
        self.timeseries_path = path
        with open(self.timeseries_path, "r", encoding="utf-8-sig") as f:
            self.timeseries = np.genfromtxt(f, dtype=float, delimiter=",")
        self.timeseries_loaded.emit()
