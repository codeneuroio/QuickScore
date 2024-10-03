from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget


class VideoView(QWidget):
    size_changed = pyqtSignal(int, int)

    def __init__(self, video_model, parent=None):
        super().__init__(parent)
        self.video_model = video_model
        self.max_height = None

        # Components
        self.video_widget = QVideoWidget(self)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video_widget)
        self.setLayout(layout)

        # Initialize
        self.video_model.set_video_output(self.video_widget)

        # Connect signals
        self.video_model.video_loaded.connect(self.resize_video)

    def set_max_height(self, height):
        self.max_height = height

    def resize_video(self):
        width = self.video_model.video_width
        height = self.video_model.video_height

        if self.max_height and height > self.max_height:
            aspect_ratio = width / height
            height = self.max_height
            width = int(height * aspect_ratio)

        self.video_widget.setFixedSize(width, height)
        self.setFixedSize(width, height)
        self.size_changed.emit(width, height)
