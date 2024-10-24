import csv
import os
from dataclasses import asdict, replace
from typing import List, Optional
import numpy as np
from PyQt5.QtCore import QObject
from app.state.app_state import EventState
from app.utils.schema import Event


class EventModel(QObject):
    def __init__(self, state_manager):
        super().__init__()
        self._state_manager = state_manager

    @property
    def event_state(self) -> EventState:
        return self._state_manager.get_state().event

    def load_events(self):
        path = self.event_state.path
        fps = self._state_manager.get_state().video.fps

        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                raw_events = np.genfromtxt(f, dtype=float, delimiter=",")
                events = [
                    Event(idx=i, frame=int(t * fps), time=t, original_time=t)
                    for i, t in enumerate(raw_events)
                ]

            self._state_manager.update_state(
                event=EventState(
                    loaded=True, path=path, events=events, current_event_idx=0
                )
            )
            return True
        except Exception as e:
            print(f"Error loading events: {e}")
            state = replace(self.event_state, loaded=False)
            self._state_manager.update_state(event=state)
            return False

    def get_events(self):
        return self.event_state.events.copy()

    def get_current_event(self):
        idx = self.event_state.current_event_idx
        return self.event_state.events[idx]

    def get_n_events(self):
        return len(self.event_state.events)

    def _set_events(self, events: List[Event]):
        updated_state = replace(self.event_state, events=events)
        self._state_manager.update_state(event=updated_state)
        self.save_events()

    def _set_current_event_idx(self, idx: int):
        updated_state = replace(self.event_state, current_event_idx=idx)
        self._state_manager.update_state(event=updated_state)
        self.save_events()

    def set_current_event_idx(self, idx: int):
        self._set_current_event_idx(idx)

    def increment_event(self):
        idx = self.event_state.current_event_idx
        if idx < self.get_n_events() - 1:
            self._set_current_event_idx(idx + 1)

    def decrement_event(self):
        idx = self.event_state.current_event_idx
        if 0 < idx:
            self._set_current_event_idx(idx - 1)

    def create_event(self, time: float):
        current_event = self.get_current_event()
        idx = current_event.idx
        fps = self._state_manager.get_state().video.fps

        # Create new event
        new_time = current_event.time + time
        new_idx = idx + (1 if time >= 0 else 0)
        if new_time < 0:
            print("Cannot create an event before time zero")
            return

        new_event = Event(
            idx=new_idx,
            frame=int(round(new_time * fps)),
            time=new_time,
            original_time=np.nan,
        )

        # Update events list
        events = self.get_events()
        events.insert(new_idx, new_event)
        for i in range(new_idx + 1, len(events)):
            events[i].idx = i

        self._set_events(events)

        # Update current event idx
        if time < 0:
            self._set_current_event_idx(new_idx)
        else:
            self.save_events()

    def update_event_time(self, relative_time: float):
        events = self.get_events()
        current_event = self.get_current_event()
        idx = current_event.idx
        fps = self._state_manager.get_state().video.fps

        new_time = current_event.time + relative_time
        new_frame = int(round(new_time * fps))
        if new_time >= 0:
            updated_event = replace(current_event, time=new_time, frame=new_frame)
            events[idx] = updated_event
            self._set_events(events)
        else:
            print("Cannot move an event before time zero.")

    def flag_event(self):
        events = self.get_events()
        current_event = self.get_current_event()
        idx = current_event.idx

        updated_event = replace(
            current_event, is_flagged=(not current_event.is_flagged)
        )
        events[idx] = updated_event
        self._set_events(events)

    def discard_event(self):
        events = self.get_events()
        current_event = self.get_current_event()
        idx = current_event.idx

        updated_event = replace(
            current_event, is_discarded=(not current_event.is_discarded)
        )
        events[idx] = updated_event
        self._set_events(events)

    def label_event(self, label: str):
        events = self.get_events()
        current_event = self.get_current_event()
        idx = current_event.idx

        updated_event = replace(current_event, label=label)
        events[idx] = updated_event
        self._set_events(events)

    def get_output_path(self):
        video_path = self._state_manager.get_state().video.path
        return os.path.splitext(video_path)[0] + "_qs.csv"

    def save_events(self) -> None:
        events = self.get_events()
        idx = self.event_state.current_event_idx
        output_path = self.get_output_path()
        with open(output_path, "w", newline="") as csvfile:
            fieldnames = [
                "id",
                "time",
                "original_time",
                "label",
                "is_flagged",
                "is_discarded",
                "is_current",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for event in events:
                event_dict = asdict(event)
                event_dict["is_current"] = event.idx == idx
                event_dict["id"] = event_dict.pop("idx")

                # Remove any keys not in fieldnames
                event_dict = {k: v for k, v in event_dict.items() if k in fieldnames}

                writer.writerow(event_dict)

    def load_events_from_internal_file(self):
        file_path = self.get_output_path()
        with open(file_path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            new_events: List[Event] = []
            current_event_idx: Optional[int] = None
            fps = self._state_manager.get_state().video.fps

            for row in reader:
                event = Event(
                    idx=int(row["id"]),
                    time=float(row["time"]),
                    frame=int(round(float(row["time"]) * fps)),
                    original_time=float(row["original_time"]),
                    label=str(row["label"]),
                    is_flagged=row["is_flagged"].lower() == "true",
                    is_discarded=row["is_discarded"].lower() == "true",
                )
                new_events.append(event)

                if row["is_current"].lower() == "true":
                    current_event_idx = event.idx

        self._set_events(new_events)
        if current_event_idx is not None:
            self._set_current_event_idx(current_event_idx)
        elif new_events:
            self._set_current_event_idx(0)
