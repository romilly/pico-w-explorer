# This example shows you how you can use Pico W Explorer's speaker to play different notes and string them together into a bleepy tune.
# It uses code written by Avram Piltch - check out his Tom's Hardware article! https://www.tomshardware.com/uk/how-to/buzzer-music-raspberry-pi-pico

import time
from picographics import PicoGraphics, DISPLAY_PICO_W_EXPLORER
from pimoroni import Speaker
from machine import Pin
from chromatic import frequency_for_note

display = PicoGraphics(display=DISPLAY_PICO_W_EXPLORER)

# pull GP8 high to enable speaker
amp_en = Pin(8, Pin.OUT)
amp_en.on()

# Create a speaker on pin 22
speaker = Speaker(22)

# constants
BLACK = display.create_pen(0, 0, 0)
GREEN = display.create_pen(0, 255, 0)

WIDTH, HEIGHT = display.get_bounds()

VOLUME = 0.4



# put the notes for your song in here!
song = ["AS6", "A6", "AS6", "P", "AS5", "P", "AS5", "P", "F6", "DS6", "D6", "F6", "AS6", "A6", "AS6", "D7", "C7", "AS6", "C7", "P", "C6", "P", "C6", "P", "C6", "AS5", "A5", "C6", "F6", "P", "F6", "P", "G6", "A6", "AS6", "A6", "G6", "F6", "G6", "F6", "DS6", "D6", "DS6", "D6", "C6", "AS5", "AS5", "A5", "G5", "F5", "G5", "AS5", "A5", "C6", "AS5", "D6", "C6", "DS6", "D6", "P", "AS5", "P", "AS5"]


def clear():                        # this function clears Pico W Explorer's screen to black
    display.set_pen(BLACK)
    display.clear()
    display.update()


def playtone(frequency):            # this function tells your program how to make noise
    speaker.set_tone(frequency, VOLUME)


def bequiet():                      # this function tells your program how not to make noise
    speaker.set_tone(-1)


def playsong(song):                 # this function plays your song
    a = 0                           # this variable keeps track of the visualiser bars
    for i in range(len(song)):
        if (song[i] == "P"):
            bequiet()
        else:
            freq = frequency_for_note(song[i])
            print(song[i], freq)
            playtone(frequency_for_note(song[i]))
            display.set_pen(GREEN)  # switch to green pen
            display.rectangle(a, HEIGHT - int(frequency_for_note(song[i]) / 21), 5, HEIGHT)  # draw a green bar corresponding to the frequency of the note
            a += 7
        if a >= WIDTH:  # clears the screen if the green bars reach the right hand edge
            clear()
            a = 0
        display.update()
        time.sleep(0.15)  # change this number if you want to alter how long the notes play for
    bequiet()


clear()
playsong(song)
clear()
