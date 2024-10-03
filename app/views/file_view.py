import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QWidget


class FileView(QWidget):
    video_selected = pyqtSignal(str)
    events_selected = pyqtSignal(str)
    timeseries_selected = pyqtSignal(str)

    def __init__(self, video_model, events_model, timeseries_model):
        super().__init__()
        self.video_model = video_model
        self.events_model = events_model
        self.timeseries_model = timeseries_model
        self.default_dir = ""

    def select_video(self):
        video_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            self.default_dir,
            filter="Videos (*.mp4 *.avi *.mov *.flv *.wmv)",
        )
        if video_path:
            self.default_dir = os.path.dirname(video_path)
            self.video_model.load_video(video_path)
            self.video_selected.emit(video_path)
        return video_path

    def select_events(self):
        events_path, _ = QFileDialog.getOpenFileName(
            self, "Select Events File", self.default_dir, filter="CSV Files (*.csv)"
        )
        if events_path:
            self.events_model.load_events(events_path)
            self.events_selected.emit(events_path)
        return events_path

    def select_timeseries(self):
        timeseries_path, _ = QFileDialog.getOpenFileName(
            self, "Select Timeseries File", self.default_dir, filter="CSV Files (*.csv)"
        )
        if timeseries_path:
            self.timeseries_model.load_timeseries(timeseries_path)
            self.timeseries_selected.emit(timeseries_path)
        return timeseries_path
