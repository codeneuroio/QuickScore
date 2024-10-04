from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from state.app_state import EventState


class EventView(QWidget):
    def __init__(self, state_manager, event_model, parent=None):
        super().__init__(parent)
        self._state_manager = state_manager
        self._event_model = event_model

        # Components
        self.event_label = QLabel()
        self.set_event_label(0, 0)
        self.event_slider = QSlider(QtCore.Qt.Horizontal)
        self.event_slider.setFixedWidth(600)
        self.event_slider.setSingleStep(1)
        self.event_slider.setTickInterval(1)
        self.event_slider.setTickPosition(QSlider.TicksBelow)
        self.event_slider.setEnabled(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.event_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.event_slider)
        self.setLayout(layout)

        # Signals
        self._state_manager.state_changed.connect(self._on_state_changed)
        self.event_slider.sliderMoved.connect(self._on_slider_moved)
        self.event_slider.sliderReleased.connect(self._on_slider_released)

    @property
    def event_state(self) -> EventState:
        return self._state_manager.get_state().event

    def _on_state_changed(self, state):
        if state.playback.files_loaded:
            self.event_slider.setEnabled(True)

        event_state = state.event
        if event_state.loaded:
            self._update_view(event_state)

    def _update_view(self, event_state: EventState):
        self.set_event_label(
            event_state.current_event.idx, len(self._event_model.events)
        )
        self.set_event_slider_position(event_state.current_event.idx)
        self.set_event_slider_range(len(self._event_model.events) - 1)

    def set_event_label(self, curr: int, n_events: int):
        self.event_label.setText(f"Event {curr} of {n_events}")

    def set_event_slider_position(self, position: int):
        self.event_slider.setValue(position)

    def set_event_slider_range(self, maximum: int):
        self.event_slider.setRange(0, maximum)

    def _on_slider_moved(self, value: int):
        self.set_event_label(value, len(self._event_model.events))

    def _on_slider_released(self):
        value = self.event_slider.value()
        self._event_model.set_current_event(value)
