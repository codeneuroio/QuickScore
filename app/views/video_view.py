from PyQt5 import QtMultimediaWidgets, QtWidgets
from PyQt5.QtCore import QPointF, QRectF, QSizeF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QTransform


class VideoView(QtWidgets.QGraphicsView):
    rectangle_changed = pyqtSignal(QRectF)

    def __init__(self, video_model, parent=None):
        super().__init__(parent)
        self.video_model = video_model

        self.setScene(QtWidgets.QGraphicsScene(self))
        self.videoItem = QtMultimediaWidgets.QGraphicsVideoItem()
        self.scene().addItem(self.videoItem)
        self.video_model.set_video_output(self.videoItem)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignCenter)
