import cv2
from PyQt5.QtCore import QObject, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class VideoModel(QObject):
    durationChanged = pyqtSignal(int)
    positionChanged = pyqtSignal(int)
    stateChanged = pyqtSignal(QMediaPlayer.State)
    mediaChanged = pyqtSignal()
    video_loaded = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._media_player = QMediaPlayer()
        self._media_player.durationChanged.connect(self._on_duration_changed)
        self._media_player.positionChanged.connect(self._on_position_changed)
        self._media_player.stateChanged.connect(self.stateChanged)

        self.video_path = ""
        self.video_object = None
        self.fps = 0
        self.video_height = 0
        self.video_width = 0
        self.video_n_frames = 0

    def _on_duration_changed(self, duration: int):
        self.durationChanged.emit(duration)

    def _on_position_changed(self, position: int):
        self.positionChanged.emit(position)

    def load_video(self, path):
        self.video_path = path
        self.set_media(path)

        # Load video metadata using cv2
        self.video_object = cv2.VideoCapture(self.video_path)
        self.fps = self.video_object.get(cv2.CAP_PROP_FPS)
        self.video_height = int(self.video_object.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_width = int(self.video_object.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_n_frames = int(self.video_object.get(cv2.CAP_PROP_FRAME_COUNT))

        self.video_loaded.emit(self.video_path)

    def set_media(self, path):
        self._media_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaChanged.emit()

    def set_video_output(self, video):
        self._media_player.setVideoOutput(video)

    def play(self):
        self._media_player.play()

    def pause(self):
        self._media_player.pause()

    def stop(self):
        self._media_player.stop()

    def set_position(self, position):
        self._media_player.setPosition(position)

    def get_position(self):
        return self._media_player.position()

    def get_duration(self):
        return self._media_player.duration()

    def get_state(self):
        return self._media_player.state()

    def get_media_player(self):
        return self._media_player

    def toggle_state(self):
        state = self.get_state()
        if state == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def get_frame(self, timestamp):
        if self.video_object is None:
            return None

        frame_number = int(timestamp * self.fps)
        self.video_object.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.video_object.read()
        if ret:
            return frame
        else:
            return None

    def close_video(self):
        if self.video_object is not None:
            self.video_object.release()
        self._media_player.setMedia(QMediaContent())
        self.video_path = ""
        self.fps = 0
        self.video_height = 0
        self.video_width = 0
        self.video_n_frames = 0
