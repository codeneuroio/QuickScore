from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class EventView(QWidget):
    def __init__(self, event_model, parent=None):
        super().__init__(parent)
        self.event_model = event_model

        # Components
        self.event_label = QLabel(f"Event {self.event_model.event_id} of {len(self.event_model.events)}")
        self.event_slider = QSlider(QtCore.Qt.Horizontal)
        self.event_slider.setFixedWidth(600)
        self.event_slider.setSingleStep(1)
        self.event_slider.setTickInterval(1)
        self.event_slider.setTickPosition(QSlider.TicksBelow)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.event_label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.event_slider)

        # Initial state
        self.set_event_slider_enabled(True)
        self.set_event_slider_position()
        self.set_event_slider_range()

        # Signals
        self.event_slider.valueChanged.connect(self.set_event_slider_position)

    def set_event_slider_enabled(self, enabled: bool = False):
        self.event_slider.setEnabled(enabled)

    def set_event_slider_position(self, position: int = 0):
        self.event_slider.setValue(0)

    def set_event_slider_range(self, max: int = 20):
        self.event_slider.setRange(0, max)
