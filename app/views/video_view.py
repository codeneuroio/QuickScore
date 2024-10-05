from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from state.app_state import VideoState


class VideoView(QWidget):

    def __init__(self, state_manager, video_model, parent=None):
        super().__init__(parent)
        self._state_manager = state_manager
        self._video_model = video_model
        self.max_height = None

        # Components
        self.video_widget = QVideoWidget(self)
        self._video_model.set_video_output(self.video_widget)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video_widget)
        self.setLayout(layout)

        # State
        self._state_manager.state_changed.connect(self._on_state_changed)

    @property
    def video_state(self) -> VideoState:
        return self._state_manager.get_state().video

    def _on_state_changed(self, state):
        if state.video.loaded:
            self._resize_video()

        if state.playback.is_playing:
            self._video_model.handle_play()
        else:
            self._video_model.pause()

    def _resize_video(self):
        width, height = self.video_state.width, self.video_state.height

        if self.max_height and height > self.max_height:
            aspect_ratio = width / height
            height = self.max_height
            width = int(height * aspect_ratio)

        self.video_widget.setFixedSize(width, height)
        self.setFixedSize(width, height)

    def set_max_height(self, height):
        self.max_height = height
