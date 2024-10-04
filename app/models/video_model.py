import cv2
from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from state.app_state import VideoState


class VideoModel(QObject):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self._media_player = QMediaPlayer()
        self.video_object = None

    @property
    def video_state(self) -> VideoState:
        return self.state_manager.get_state().video

    def load_video(self, path):
        try:
            self.video_object = cv2.VideoCapture(path)
            width = int(self.video_object.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.video_object.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.video_object.get(cv2.CAP_PROP_FPS)
            if not fps.is_integer():
                raise ArithmeticError("FPS is not an integer.")
            fps = int(fps)

            self.set_media(path)
            self.state_manager.update_state(
                video=VideoState(
                    loaded=True, path=path, fps=fps, width=width, height=height
                )
            )
            return True
        except Exception as e:
            print(f"Error loading video: {e}")
            self.state_manager.update_state(video=VideoState(loaded=False))
            return False

    def set_media(self, path):
        self._media_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.set_position(0)
        self.play()
        self.pause()

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

    def get_play_state(self):
        return self._media_player.state()

    def get_media_player(self):
        return self._media_player

    def toggle_state(self):
        state = self.get_play_state()
        if state == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def get_frame(self, timestamp):
        if self.video_object is None:
            return None

        frame_number = int(timestamp * self.video_state.fps)
        self.video_object.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.video_object.read()
        if ret:
            return frame
        else:
            return None
