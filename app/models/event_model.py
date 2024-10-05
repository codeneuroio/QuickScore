from dataclasses import replace
from typing import List
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from state.app_state import EventState
from utils.schema import Event


class EventModel(QObject):
    event_created = pyqtSignal()

    def __init__(self, state_manager):
        super().__init__()
        self._state_manager = state_manager
        self.events: List[Event] = []
        self.n_events: int = 0

    @property
    def event_state(self) -> EventState:
        return self._state_manager.get_state().event

    def load_events(self, path: str):
        fps = self._state_manager.get_state().video.fps

        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                raw_events = np.genfromtxt(f, dtype=float, delimiter=",")
                self.events = [
                    Event(idx=i, frame=int(t * fps), time=t, original_time=t)
                    for i, t in enumerate(raw_events)
                ]
                self.n_events = len(self.events)

            self._state_manager.update_state(
                event=EventState(loaded=True, path=path, current_event=self.events[0])
            )
            return True
        except Exception as e:
            print(f"Error loading events: {e}")
            state = replace(self.event_state, loaded=False)
            self._state_manager.update_state(event=state)
            return False

    def _update_event_state(self, event: Event):
        updated_state = replace(self.event_state, current_event=event)
        self._state_manager.update_state(event=updated_state)

    def set_current_event(self, idx: int):
        next_event = self.events[idx]
        self._update_event_state(next_event)

    def increment_event(self):
        current_event = self.event_state.current_event
        if current_event.idx < self.n_events - 1:
            next_event = self.events[current_event.idx + 1]
            self._update_event_state(next_event)

    def decrement_event(self):
        current_event = self.event_state.current_event
        if 0 < current_event.idx:
            prev_event = self.events[current_event.idx - 1]
            self._update_event_state(prev_event)

    def create_event(self, time: float):
        current_event = self.event_state.current_event
        fps = self._state_manager.get_state().video.fps

        # Create new event
        new_time = current_event.time + time
        new_index = current_event.idx + (1 if time >= 0 else 0)
        if new_time < 0:
            print("Cannot create an event before time zero")
            return

        new_event = Event(
            idx=new_index,
            frame=int(round(new_time * fps)),
            time=new_time,
            original_time=np.nan,
        )

        # Update events list
        self.events.insert(new_index, new_event)
        self.n_events += 1
        for i in range(new_index + 1, len(self.events)):
            self.events[i].idx = i

        # Update current event state
        if time < 0:
            updated_event = replace(current_event, idx=new_index)
            self._update_event_state(updated_event)

        self.event_created.emit()

    def update_event_time(self, relative_time: float):
        current_event = self.event_state.current_event
        fps = self._state_manager.get_state().video.fps

        new_time = current_event.time + relative_time
        new_frame = int(round(new_time * fps))
        if new_time >= 0:
            updated_event = replace(current_event, time=new_time, frame=new_frame)
            self.events[current_event.idx] = updated_event
            self._update_event_state(updated_event)
        else:
            print("Cannot move an event before time zero.")
