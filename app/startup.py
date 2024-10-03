import sys
from models import EventModel, TimeSeriesModel, VideoModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QGridLayout,
    QMainWindow,
    QWidget,
)
from views import EventView, FileView, PlaybackView, TimeSeriesView, VideoView


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        _, _, self.screen_width, self.screen_height = (
            QDesktopWidget().screenGeometry(-1).getRect()
        )
        self.setGeometry(
            int(0.25 * self.screen_width),
            int(0.16 * self.screen_height),
            int(0.50 * self.screen_width),
            int(0.67 * self.screen_height),
        )
        self.setWindowTitle("QuickScore")
        self.hotkeys = {}

        # Models
        self.video_model = VideoModel()
        self.event_model = EventModel()
        self.timeseries_model = TimeSeriesModel()

        # Views
        self.file_view = FileView(
            self.video_model, self.event_model, self.timeseries_model
        )
        self.video_view = VideoView(self.video_model)
        self.playback_view = PlaybackView()
        self.event_view = EventView(self.event_model)
        self.timeseries_view = TimeSeriesView(self.timeseries_model)

        # Layout
        main_layout = QGridLayout()
        main_layout.addWidget(self.video_view, 0, 0, 8, 9, alignment=Qt.AlignCenter)
        main_layout.addWidget(
            self.timeseries_view.plot_window, 8, 0, 1, 9, alignment=Qt.AlignCenter
        )
        main_layout.addLayout(
            self.event_view.layout, 9, 0, 1, 9, alignment=Qt.AlignCenter
        )
        main_layout.addLayout(self.playback_view.layout, 11, 1, 1, 7)
        main_layout.setRowStretch(0, 10)
        main_layout.setRowStretch(7, 2)
        main_layout.setRowStretch(9, 1)
        main_layout.setRowStretch(11, 1)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Setup
        self.video_view.set_max_height(int(self.screen_height * 0.5))
        self.setup_hotkeys()
        self.setup_signals()

    def setup_signals(self):
        # File Selection
        # self.file_view.video_path_changed.connect(self.video_model.set_media)
        pass

    def setup_hotkeys(self):
        self.hotkeys = {
            Qt.Key_1: self.file_view.select_video,
            Qt.Key_2: self.file_view.select_events,
            Qt.Key_3: self.file_view.select_timeseries,
        }

    def keyPressEvent(self, event):
        # TODO remove mock data
        if event.key() == Qt.Key_1:
            self.video_model.load_video("/Users/Ryan/Downloads/EPT001_N1_1_intensity_low.mp4")
            return
        if event.key() == Qt.Key_2:
            self.event_model.load_events("/Users/Ryan/Downloads/EPT_events.csv")
            return
        if event.key() == Qt.Key_3:
            self.timeseries_model.load_timeseries("/Users/Ryan/Downloads/EPT_ts.csv")
            return

        # END TODO

        key = event.key()
        if key in self.hotkeys:
            self.hotkeys[key]()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
