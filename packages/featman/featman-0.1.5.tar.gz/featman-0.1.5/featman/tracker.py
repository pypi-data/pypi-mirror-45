"""
    This is the state tracker for the metaenv
"""
import time
from copy import deepcopy
import random
from coolname import generate_slug
from crayons import yellow, blue, green, red
from spaceman import Spaceman


__STEPTYPES__ = ['time_seconds', 'time_minute', 'numerical']

class StateTracker(object):
    def __init__(self, state_step_type: str, state_size: int, name=generate_slug()):
        self.spaceman = Spaceman(use_step=True, step_back=1)
        self.base_query = {
            "type": "meta"
        }
        self.name = name
        self.spacing = 0
        self.query_for = None
        if state_step_type not in __STEPTYPES__:
            raise TypeError(f"State Step Type Must Be Of The Following: {__STEPTYPES__}")
        
        if state_step_type == 'time_minute':
            minute_size = 60
            self.spacing = minute_size*state_size
            self.query_for = "timestamp"
        elif state_step_type == "time_seconds":
            self.query_for = "timestamp"
            self.spacing = state_size
        else:
            self.spacing = state_size

        # We'll query for

    def submit_state(self, state, meta_data: dict):
        if self.query_for is not None:
            if self.query_for == "timestamp":
                _timestamp = meta_data.get("timestamp", None)
                # print(type(_timestamp))
                if _timestamp is None:
                    raise AttributeError("Missing timestamp in metadata")
        new_data = {
            "symbol": meta_data["bar"]["symbol"],
            "session_id": meta_data["bar"]["session_id"],
            "timestamp": meta_data["timestamp"],
            "trackid": meta_data["trackid"]
        }
        
        query = {**self.base_query, **new_data}

        with self.spaceman as space:
            space.store(state, query=query, current_time=False)
    
    def get_last_state(self, meta_data: dict):
        # print(meta_data)
        is_before = False
        if self.query_for is not None:
            if self.query_for == "timestamp":
                _timestamp = meta_data.get("timestamp", None)
                if _timestamp is None:
                    raise AttributeError("Missing timestamp in metadata")
                else:
                    is_before = True
        new_data = {
            "symbol": meta_data["bar"]["symbol"],
            "timestamp": meta_data["timestamp"],
            "trackid": meta_data["trackid"],
            "session_id": meta_data["bar"]["session_id"],
        }
        query = {**self.base_query, **new_data}
        # print(f"is_before: {is_before}. Spacing: {self.spacing}, Timestamp: {new_data['timestamp']}" )
        with self.spaceman as space:
            latest = space.load(query=query, is_before=is_before, seconds=self.spacing)
            return latest
        return None


if __name__ == "__main__":
    track = StateTracker(state_step_type="time_minute", state_size=30)
    num_mins = 300
    current_time = round(time.time())
    # print(track)
    meta_info = {
        "type": "meta",
        "slug": generate_slug(),
        "timestamp": 0.0
    }
    # This is basically the core loop
    # The core loop will get the most recent time and push that as the current "timestamp" for the portfolio observation each iteration.
    for _min in reversed(range(num_mins)):
        latest_time = current_time - (60 * _min)
        state = random.randint(1, 100)
        meta_info["timestamp"] = float(latest_time)
        track.submit_state(state, meta_info)
        latest = track.get_last_state(meta_info)
        if latest is not None:
            reward = state-latest
            s = blue(state, bold=random.choice([True, False]))
            # a = client.get_action(state)
            r = green(reward, bold=random.choice([True, False]))
            
            _s = red(latest, bold=random.choice([True, False]))
            
            
            print(
                f"Last state: {_s} Current State: {s}, Reward: {r}"
            )
