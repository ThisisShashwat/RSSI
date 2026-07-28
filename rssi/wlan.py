import ctypes
from ctypes import wintypes, byref, cast, POINTER

wlanapi = ctypes.WinDLL("wlanapi.dll")

class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD), ("Data4", ctypes.c_ubyte * 8)]

class WLAN_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [("InterfaceGuid", GUID),
                ("strInterfaceDescription", wintypes.WCHAR * 256),
                ("isState", wintypes.DWORD)]

class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [("dwNumberOfItems", wintypes.DWORD), ("dwIndex", wintypes.DWORD),
                ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)]

RSSI_OPCODE = 0x10000102  # wlan_intf_opcode_rssi

def open_handle():
    ver, h = wintypes.DWORD(), wintypes.HANDLE()
    wlanapi.WlanOpenHandle(2, None, byref(ver), byref(h))
    return h

def get_first_interface_guid(handle):
    info_ptr = POINTER(WLAN_INTERFACE_INFO_LIST)()
    wlanapi.WlanEnumInterfaces(handle, None, byref(info_ptr))
    guid = info_ptr.contents.InterfaceInfo[0].InterfaceGuid
    wlanapi.WlanFreeMemory(info_ptr)
    return guid

def get_rssi_dbm(handle, guid):
    size, data_ptr, opcode = wintypes.DWORD(), ctypes.c_void_p(), ctypes.c_uint()
    ret = wlanapi.WlanQueryInterface(handle, byref(guid), RSSI_OPCODE,
                                      None, byref(size), byref(data_ptr), byref(opcode))
    if ret != 0 or not data_ptr.value:
        return None
    rssi = cast(data_ptr, POINTER(ctypes.c_long)).contents.value
    wlanapi.WlanFreeMemory(data_ptr)
    return rssi
