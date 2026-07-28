from collections import deque
import numpy as np

class PresenceDetector:
    def __init__(self, window=30, absent_var=0.5, motion_delta=1.5, hysteresis=3):
        self.buf = deque(maxlen=window)
        self.state = "absent"
        self.absent_var = absent_var
        self.motion_delta = motion_delta
        self._pending = None
        self._pending_count = 0
        self.hysteresis = hysteresis

    def update(self, rssi):

        if rssi is None:
            return self.state

        self.buf.append(rssi)
        if len(self.buf) < 4:
            print(len(self.buf))
            return self.state

        arr = np.array(self.buf)
        var = arr.var()
        motion = np.mean(np.abs(np.diff(arr)))

        print("yo", var, motion)

        if var < self.absent_var:
            new_state = "absent"
        elif motion > self.motion_delta:
            new_state = "moving"
        else:
            new_state = "still"


        if new_state == self._pending:
            self._pending_count += 1
        else:
            self._pending = new_state
            self._pending_count = 1

        if self._pending_count >= self.hysteresis:
            self.state = new_state

        return self.state



