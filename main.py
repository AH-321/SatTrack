from tracking import tracker
try:
    import serial
except Exception:
    serial = None
    print("pyserial not installed; serial controller disabled. Install with 'pip install pyserial' to enable hardware output.")
import time
import gui

controller = None
if serial:
    try:
        # Update this to the correct port for your OS (e.g., '/dev/ttyUSB0' or 'COM3')
        controller = serial.Serial('/dev/ttyUSB0', 9600)
    except Exception as e:
        controller = None
        print(f"Unable to open serial port: {e}")

def init():
    gui.init()

def main():
    while True:

        azimuth, elevation, distance, sat_name = tracker.fetch()

        msg = f"{azimuth.degrees:.2f},{elevation.degrees:.2f}\n"
        if controller:
            try:
                controller.write(msg.encode('utf-8'))
            except Exception as e:
                print(f"Serial write failed: {e}")

init()