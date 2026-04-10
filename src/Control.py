from evdev import InputDevice, categorize, ecodes
from threading import Thread
from Hexapod import HexState, Hexapod
import atexit
import board
import digitalio
import time

# Update to your controller's event device
device = InputDevice('/dev/input/event5')
stop = False
stopServos = digitalio.DigitalInOut(board.D4)
stopServos.direction = digitalio.Direction.OUTPUT
stopServos.value = False

# Initialize state holders
key_states = {}
abs_states = {}

# Mapping known button/axis names for better display
KEY_NAMES = {
    ecodes.BTN_SOUTH: 'X',
    ecodes.BTN_EAST: 'O',
    ecodes.BTN_NORTH: '△',
    ecodes.BTN_WEST: '☐',
    ecodes.BTN_TL: 'L1',
    ecodes.BTN_TR: 'R1',
    ecodes.BTN_TL2: 'L2',
    ecodes.BTN_TR2: 'R2',
    ecodes.BTN_SELECT: 'Share',
    ecodes.BTN_START: 'Options',
    ecodes.BTN_THUMBL: 'L3',
    ecodes.BTN_THUMBR: 'R3',
    ecodes.BTN_MODE: 'PS',
    ecodes.BTN_TOUCH: 'Touchpad'
}

ABS_NAMES = {
    ecodes.ABS_X: 'Left Stick X',
    ecodes.ABS_Y: 'Left Stick Y',
    ecodes.ABS_RX: 'Right Stick X',
    ecodes.ABS_RY: 'Right Stick Y',
    ecodes.ABS_Z: 'L2 Trigger',
    ecodes.ABS_RZ: 'R2 Trigger',
    ecodes.ABS_HAT0X: 'D-Pad X',
    ecodes.ABS_HAT0Y: 'D-Pad Y'
}

def shut_down():
    time.sleep(0.5)
    hex.set_state(HexState.IDLE)
    i = 0
    while i < hex.maxIndex:
        hex.update()
        i = i+1
    time.sleep(0.5)

def reader():
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_states[event.code] = event.value
        elif event.type == ecodes.EV_ABS:
            abs_states[event.code] = event.value

atexit.register(shut_down)
Thread(target=reader, daemon=True).start()
hex = Hexapod()
while not stop:
    hex.update()
    ps = key_states.get(ecodes.BTN_MODE, 0)
    if ps == 1:
        stop = True

    stand = key_states.get(ecodes.BTN_SOUTH, 0)
    if stand == 1:
        hex.set_state(HexState.STANDING)

    amount = abs_states.get(ecodes.ABS_HAT0Y, 0)
    hex.adjustHeight(-amount)

    sit = key_states.get(ecodes.BTN_NORTH, 0)
    if sit == 1:
        hex.set_state(HexState.IDLE)

    directionVector = (int(abs_states.get(ecodes.ABS_RX, 0)),int(abs_states.get(ecodes.ABS_RY, 0)))
    hex.setDirectionVector(directionVector)

    rotateVelocity = (int(abs_states.get(ecodes.ABS_X, 0)))
    hex.setRotationVelocity(rotateVelocity)


