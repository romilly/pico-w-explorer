import network
import WIFI_CONFIG
import time

max_wait = 10
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_CONFIG.SSID, WIFI_CONFIG.PASSWORD)
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        print('connected')
        break
max_wait -= 1
time.sleep(1)
if wlan.status() != 3:
    print('network connection failed')