import time

from mqtt_publish import StatePublisher
from wlan import *
from detector import PresenceDetector

HZ = 10

DEVICE_ID = "desktop-pc"
BROKER = "192.168.0.10"

det = PresenceDetector(window=30, motion_delta=0.25, absent_var=0.3)

try:
    pub = StatePublisher(DEVICE_ID, BROKER)
except: pass

handle = open_handle()
guid = get_first_interface_guid(handle)


RSSI_MIN, RSSI_MAX = -90, -30
BAR_WIDTH = 30

seen_min = None
seen_max = None


def render(rssi, state):
    global seen_min, seen_max

    if rssi is None:
        bar = "-" * BAR_WIDTH
        rssi_str, range_str = " -- ", "?-?"
    else:
        seen_min = rssi if seen_min is None else min(seen_min, rssi)
        seen_max = rssi if seen_max is None else max(seen_max, rssi)

        span = seen_max - seen_min
        pct = 0.5 if span == 0 else (rssi - seen_min) / span
        filled = int(max(0.0, min(1.0, pct)) * BAR_WIDTH)
        bar = "#" * filled + "-" * (BAR_WIDTH - filled)
        rssi_str = f"{rssi:>4}"
        range_str = f"{seen_min}-{seen_max}"

    color = "\033[31m" if state == "moving" else "\033[32m"
    reset = "\033[0m"
    print(f"\r{color}[{bar}] {rssi_str} (seen {range_str})  {state:<7}{reset}", end="", flush=True)


while True:
    rssi = get_rssi_dbm(handle, guid)
    state = det.update(rssi)

    try:
        pub.publish(state)
    except Exception:
        pass

    render(rssi, state)
    time.sleep(1 / HZ)

