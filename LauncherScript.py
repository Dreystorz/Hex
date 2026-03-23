import time
import subprocess
import evdev
from evdev import InputDevice, list_devices
from evdev import InputDevice, categorize, ecodes
import sys

CONTROLLER_MAC = "4C:B9:9B:AB:41:EC"  # Controller's Bluetooth MAC address
PROGRAM_TO_RUN = "/home/andriy/Project/src/Control.py"

def is_controller_connected():
    try:
        output = subprocess.check_output(["bluetoothctl", "info", CONTROLLER_MAC]).decode()
        return "Connected: yes" in output
    except subprocess.CalledProcessError:
        return False

def find_controller():
    devices = [InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "Wireless Controller" in device.name:
            return device
    return None

def wait_for_controller():
    print("Waiting for controller to connect via Bluetooth...")
    while not is_controller_connected():
        time.sleep(1)
    print("Controller connected!")
    return find_controller()

def launch_program(device):
    device = find_controller()
    if not device:
        print("Controller not found!")
        sys.exit(1)

    print("Waiting for start button...")

    hexapod_process = None

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                if key_event.keycode == 'BTN_MODE':  # Adjust this to your desired button
                    if hexapod_process is None:
                        print("Starting hexapod script...")
                        hexapod_process = subprocess.run([sys.executable, PROGRAM_TO_RUN])
                        print("Hexapod script has ended...")
                        hexapod_process = None


if __name__ == "__main__":
    device = wait_for_controller()
    launch_program(device)