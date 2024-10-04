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
from state import StateManager
from views import EventView, TimeSeriesView, VideoView, PlaybackView, FileView


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.screen_width, self.screen_height = 0, 0
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
        # self.setup_signals()

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

    # def setup_signals(self):
    #     # Files
    #     self.file_view.video_selected.connect(self.video_model.load_video)
    #     self.file_view.events_selected.connect(self.event_model.load_events)
    #     self.file_view.timeseries_selected.connect(
    #         self.timeseries_model.load_timeseries
    #     )
    #     self.all_files_loaded.connect(self.set_initial_state)
    #
    #     # Video
    #     self.video_model.video_loaded.connect(self.check_files_loaded)
    #     self.video_model.fps_changed.connect(self.event_model.update_fps)
    #     self.video_model.fps_changed.connect(self.timeseries_model.update_fps)
    #
    #     # Playback
    #     self.playback_view.next_button_pressed.connect(self.event_model.increment_event)
    #     self.playback_view.prev_button_pressed.connect(self.event_model.decrement_event)
    #
    #     # Events
    #     self.event_model.events_loaded.connect(self.check_files_loaded)
    #     self.event_model.event_created.connect(self.event_view.on_events_updated)
    #     self.event_model.event_updated.connect(self.timeseries_view.update_plot)
    #
    #     # TimeSeries
    #     self.timeseries_model.timeseries_loaded.connect(self.check_files_loaded)
    #     self.timeseries_view.vline_updated.connect(self.event_model.update_event_time)
    #     self.timeseries_view.tmp_vline_created.connect(self.event_model.create_event)

    def setup_hotkeys(self):
        self.hotkeys = {
            Qt.Key_1: self.file_view.select_video,
            Qt.Key_2: self.file_view.select_events,
            Qt.Key_3: self.file_view.select_timeseries,
            # Qt.Key_Left: self.playback_view.prev_button_pressed,
            # Qt.Key_Right: self.playback_view.next_button_pressed,
            # Qt.Key_Alt: self.timeseries_view.create_tmp_vline,
        }

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

        key = event.key()
        if key in self.hotkeys:
            self.hotkeys[key]()
        else:
            super().keyPressEvent(event)

    # def keyReleaseEvent(self, event):
    #     if event.key() == Qt.Key_Alt:
    #         self.timeseries_view.destroy_tmp_vline()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
