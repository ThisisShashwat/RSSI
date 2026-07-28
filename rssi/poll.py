import time
from wlan import *

HZ = 10

handle = open_handle()
guid = get_first_interface_guid(handle)

while True:
    rssi = get_rssi_dbm(handle, guid)
    print(rssi)
    time.sleep(1/ HZ)