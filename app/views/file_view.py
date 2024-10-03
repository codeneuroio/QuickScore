import csv
import os
import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QWidget


class FileView(QWidget):
    video_path_changed = pyqtSignal(str)
    events_path_changed = pyqtSignal(str)
    timeseries_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._video_path: str = ""
        self._events_path: str = ""
        self._timeseries_path: str = ""
        self.events_array: np.ndarray = np.array([])
        self.timeseries_array: np.ndarray = np.array([])
        self.default_dir: str = ""

    # Properties
    @pyqtProperty(str, notify=video_path_changed)
    def video_path(self):
        return self._video_path

    @pyqtProperty(str, notify=events_path_changed)
    def events_path(self):
        return self._events_path

    @pyqtProperty(str, notify=timeseries_path_changed)
    def timeseries_path(self):
        return self._timeseries_path

    # Setters
    @video_path.setter
    def video_path(self, value):
        if self._video_path != value:
            self._video_path = value
            self.video_path_changed.emit(value)

    @events_path.setter
    def events_path(self, value):
        if self._events_path != value:
            self._events_path = value
            self.events_path_changed.emit(value)

    @timeseries_path.setter
    def timeseries_path(self, value):
        if self._timeseries_path != value:
            self._timeseries_path = value
            self.timeseries_path_changed.emit(value)

    # Slots
    def select_video(self):
        video_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            self.default_dir,
            filter="Videos (*.mp4 *.avi *.mov *.flv *.wmv)",
        )
        if video_path:
            self.video_path = video_path
            self.default_dir = os.path.dirname(self.video_path)
        return self.video_path

    def select_events(self):
        events_path, _ = QFileDialog.getOpenFileName(
            self, "Select Events File", self.default_dir, filter="CSV Files (*.csv)"
        )
        if events_path:
            self.events_path = events_path
            self.events_array = self.read_csv_to_array(self.events_path)
        return self.events_path

    def select_timeseries(self):
        timeseries_path, _ = QFileDialog.getOpenFileName(
            self, "Select Timeseries File", self.default_dir, filter="CSV Files (*.csv)"
        )
        if timeseries_path:
            self.timeseries_path = timeseries_path
            self.timeseries_array = self.read_csv_to_array(self.timeseries_path)
        return self.timeseries_path

    @staticmethod
    def read_csv_to_array(file_path: str) -> np.ndarray:
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                return np.array([float(row[0]) for row in reader])
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return np.array([])
