from win32wifi import Win32Wifi

# List interfaces
interfaces = Win32Wifi.getWirelessInterfaces()
for iface in interfaces:
    print(f"Interface: {iface.description} ({iface.state_string})")

    # List available networks
    networks = Win32Wifi.getWirelessAvailableNetworkList(iface)
    for network in networks:
        print(f"  SSID: {network.ssid.decode('utf-8', 'replace')}, Signal: {network.signal_quality}%")