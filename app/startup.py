import sys
from models import EventModel, TimeSeriesModel, VideoModel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QGridLayout,
    QMainWindow,
    QWidget,
)
from state import StateManager
from views import EventView, FileView, PlaybackView, TimeSeriesView, VideoView
from dataclasses import replace


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.screen_width, self.screen_height = 0, 0
        self.playback_rate = 1.0
        self.hotkeys = {}

        # State
        self.state_manager = StateManager()

        # Models
        self.video_model = VideoModel(self.state_manager)
        self.event_model = EventModel(self.state_manager)
        self.timeseries_model = TimeSeriesModel(self.state_manager)

        # Views
        self.file_view = FileView(self.state_manager)
        self.video_view = VideoView(self.state_manager, self.video_model)
        self.event_view = EventView(self.state_manager, self.event_model)
        self.timeseries_view = TimeSeriesView(self.state_manager, self.timeseries_model)
        self.playback_view = PlaybackView(self.state_manager)

        # Setup
        self.setup_screen()
        self.setup_hotkeys()
        self.setup_signals()

    def setup_screen(self):
        self.setWindowTitle("QuickScore")
        _, _, self.screen_width, self.screen_height = (
            QDesktopWidget().screenGeometry(-1).getRect()
        )
        self.setGeometry(
            int(0.25 * self.screen_width),
            int(0.16 * self.screen_height),
            int(0.50 * self.screen_width),
            int(0.67 * self.screen_height),
        )
        self.video_view.set_max_height(int(self.screen_height * 0.5))

        # Layout
        main_layout = QGridLayout()
        main_layout.addWidget(self.video_view, 0, 0, 8, 9, alignment=Qt.AlignCenter)
        main_layout.addWidget(
            self.timeseries_view.plot_window, 8, 0, 1, 9, alignment=Qt.AlignCenter
        )
        main_layout.addWidget(self.event_view, 9, 0, 1, 9, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.playback_view, 11, 1, 1, 7)
        main_layout.setRowStretch(0, 10)
        main_layout.setRowStretch(7, 2)
        main_layout.setRowStretch(9, 1)
        main_layout.setRowStretch(11, 1)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def setup_signals(self):
        # Events
        self.event_model.event_created.connect(self.event_view.update_view)

        # TimeSeries
        self.timeseries_view.vline_updated.connect(self.event_model.update_event_time)
        self.timeseries_view.tmp_vline_created.connect(self.event_model.create_event)

        # Playback
        self.playback_view.next_button_pressed.connect(self.handle_next)
        self.playback_view.prev_button_pressed.connect(self.event_model.decrement_event)

    def handle_next(self):
        self.event_model.increment_event()
        self.start_timer()

    def setup_hotkeys(self):
        self.hotkeys = {
            Qt.Key_1: self.file_view.select_video,
            Qt.Key_2: self.file_view.select_events,
            Qt.Key_3: self.file_view.select_timeseries,
            Qt.Key_Left: self.event_model.decrement_event,
            Qt.Key_Right: self.handle_next,
            Qt.Key_Alt: self.timeseries_view.create_tmp_vline,
            Qt.Key_Comma: lambda: self.set_playback_rate(1.0),
            Qt.Key_Period: lambda: self.set_playback_rate(0.5),
            Qt.Key_Slash: lambda: self.set_playback_rate(0.25),
        }

    def start_timer(self):
        msec = int(round(1000 / self.playback_rate))
        QTimer.singleShot(msec, Qt.PreciseTimer, self.stop_timer)
        playback_state = replace(
            self.state_manager.get_state().playback, is_playing=True
        )
        self.state_manager.update_state(playback=playback_state)

    def stop_timer(self):
        playback_state = replace(
            self.state_manager.get_state().playback, is_playing=False
        )
        self.state_manager.update_state(playback=playback_state)

    def set_playback_rate(self, rate: float):
        self.playback_rate = rate
        self.video_model.set_playback_rate(self.playback_rate)
        self.timeseries_view.set_refresh_rate(self.playback_rate)

    def keyPressEvent(self, event):
        # TODO remove mock data
        if event.key() == Qt.Key_1:
            self.video_model.load_video(
                "/Users/Ryan/Downloads/EPT001_N1_1_intensity_low.mp4"
            )
            return
        if event.key() == Qt.Key_2:
            self.event_model.load_events("/Users/Ryan/Downloads/EPT_events.csv")
            return
        if event.key() == Qt.Key_3:
            self.timeseries_model.load_timeseries("/Users/Ryan/Downloads/EPT_ts.csv")
            return
        # END TODO

        if not self.state_manager.get_state().playback.is_playing:
            key = event.key()
            if key in self.hotkeys:
                self.hotkeys[key]()
            else:
                super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.timeseries_view.destroy_tmp_vline()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
