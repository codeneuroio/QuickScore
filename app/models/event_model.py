from typing import List, Optional
import numpy as np
from PyQt5.QtCore import QObject
from state.app_state import EventState
from utils.schema import Event


class EventModel(QObject):

    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.events: List[Event] = []
        self.n_events: int = 0

    @property
    def event_state(self) -> EventState:
        return self.state_manager.get_state().event

    def load_events(self, path: str):
        fps = self.state_manager.get_state().video.fps

        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                raw_events = np.genfromtxt(f, dtype=float, delimiter=",")
                self.events = [
                    Event(idx=i, frame=int(t * fps), time=t, original_time=t)
                    for i, t in enumerate(raw_events)
                ]
                self.n_events = len(self.events)

            self.state_manager.update_state(
                event=EventState(loaded=True, path=path, current_event=self.events[0])
            )
            return True
        except Exception as e:
            print(f"Error loading events: {e}")
            self.state_manager.update_state(event=EventState(loaded=False))
            return False

    # def increment_event(self):
    #     if self._current_event_index < self.n_events - 1:
    #         self._current_event_index += 1
    #         self.event_updated.emit(self.events[self._current_event_index])
    #
    # def decrement_event(self):
    #     if 0 < self._current_event_index:
    #         self._current_event_index -= 1
    #         self.event_updated.emit(self.events[self._current_event_index])
    #
    # def create_event(self, time: float):
    #     new_time = self.current_event.time + time
    #     new_index = self._current_event_index + (1 if time >= 0 else 0)
    #     if new_time < 0:
    #         print("Cannot create an event before time zero")
    #         return
    #
    #     new_event = Event(
    #         idx=new_index,
    #         frame=int(round(new_time * self.fps)),
    #         time=new_time,
    #         original_time=np.nan,
    #     )
    #
    #     # Update events
    #     self.events.insert(new_index, new_event)
    #     self.n_events += 1
    #     for i in range(new_index + 1, len(self.events)):
    #         self.events[i].idx = i
    #
    #     if time < 0:
    #         self._current_event_index += 1
    #
    #     self.event_created.emit(new_event)
    #
    # def update_event(self, **kwargs):
    #     if self.current_event:
    #         for key, value in kwargs.items():
    #             if key == "time":
    #                 new_time = self.current_event.time + value
    #                 new_frame = int(round(self.current_event.time * self.fps))
    #                 if new_time >= 0:
    #                     self.current_event.time = new_time
    #                     self.current_event.frame = new_frame
    #
    #         self.event_updated.emit(self.current_event)
    #     else:
    #         print("No current event to update")
    #
    # def update_event_time(self, relative_time: float):
    #     new_time = self.current_event.time + relative_time
    #     new_frame = int(round(new_time * self.fps))
    #     if new_time >= 0:
    #         self.current_event.time = new_time
    #         self.current_event.frame = new_frame
    #         self.event_updated.emit(self.current_event)
    #     else:
    #         print("Cannot move an event before time zero.")
    #
    # def update_fps(self, fps: int):
    #     self.fps = fps
