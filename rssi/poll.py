import time
from wlan import *
from detector import PresenceDetector

HZ = 10

det = PresenceDetector(window=30, motion_delta=0.25, absent_var=0.3)
handle = open_handle()
guid = get_first_interface_guid(handle)

while True:
    rssi = get_rssi_dbm(handle, guid)
    print(rssi)
    print(det.update(rssi))
    time.sleep(1/ HZ)