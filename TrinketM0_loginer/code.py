# Trinket Loginer program
# GNU GPL v3:
# Copyright (C) 2019  Rowdy S. "AwsomeChicken"
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import board
from digitalio import DigitalInOut, Direction, Pull
import touchio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode
import adafruit_dotstar as dotstar
import time, bfd

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D2
button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Capacitive touch on D3
touch = touchio.TouchIn(board.D3)

# HID Setup
time.sleep(1)
kbd = Keyboard()
kbd_layout = KeyboardLayoutUS(kbd)
mouse = Mouse()
######################### HELPERS ################################

def fopen():
    # open and decode the username and password
    dot[0]=(0,128,128)
    d, mod = bfd.pws()
    g=[]
    try:
        for i in d:
            # convert each char code into the correct keystroke, using the mod value
            g.append(((i+mod)//2))
    except:
        while True:
            dot[0]=(255,0,0)
            time.sleep(.5)
            dot[0]=(0,255,0)
            time.sleep(.5)
    return g

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def moveToOtherUser():
    kbd_layout.write(' ')
    time.sleep(0.75)
    # move to bottom-left corner of leftmost display
    mouse.move(x=-3700)
    mouse.move(y=2000)
    # move and click on the "OtherUser" button
    mouse.move(x=60,y=-25)
    mouse.click(Mouse.LEFT_BUTTON)

def logSeq():
    lgnfo = fopen()
    dot.brightness=.5

    dot[0] = (230,255,68)# make the dot yellow, indicate typing

    led.value = False

    for ch in lgnfo:
        kbd_layout.write(chr(ch))
        led.value = not led.value
        time.sleep(0.1)

    dot[0] = (128,128,128)# make white indicating done
    time.sleep(1)
    dot.brightness=.2
    lgnfo=""

######################### MAIN LOOP ##############################
#time.sleep(1)
# run the login before the main loop
moveToOtherUser()
logSeq()

i = 0
while True:
  # spin internal LED around! autoshow is on
  dot[0] = wheel(i & 255)
  # use D3 as capacitive touch to turn on internal LED
  if touch.value:
    #logSeq()
    dot[0] = (255, 255, 255)
    moveToOtherUser()
  led.value = touch.value
  i = (i+1) % 256  # run from 0 to 255
  time.sleep(0.01) # make bigger to slow down
