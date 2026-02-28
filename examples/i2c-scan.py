import machine


sda = machine.Pin(20)
scl = machine.Pin(21)

i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

print('scanning Explorer Base I2C bus')
devices = i2c.scan()

print(len(devices), 'device(s)')

for device in devices:
    print('address %d (0x%02x)' % (device, device))