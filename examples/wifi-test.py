import network
import time

SSID = "REDACTED_SSID"
PASSWORD = "REDACTED_PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting...")

while not wlan.isconnected():
    time.sleep(1)
    print("Still connecting...")

print("Connected!")
print("IP address:", wlan.ifconfig()[0])