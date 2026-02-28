from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(7))
pwm.freq(50)


for position in range(1000,9000,50):
    pwm.duty_u16(position)
    sleep(0.01)
for position in range(9000,1000,-50):
    pwm.duty_u16(position)
    sleep(0.01)
print('Done')