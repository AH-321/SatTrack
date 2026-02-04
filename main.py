from tracking import tracker
import os
import serial
import time
import gui

controller = None
if serial:
    if os.name == 'nt':
        port = 'COM3'
    else:
        port = '/dev/ttyUSB0'
try:
    controller = serial.Serial(port, 9600)
except Exception as e:
    controller = None
    print(f"Unable to open serial port: {e}")


def init():

    if gui.available():
        gui.init()
    else:
        print("GUI libraries not available; running in console mode.")
        tracker.init()


def send():
    while True:

        azimuth, elevation, distance, sat_name = tracker.fetch()

        msg = f"{azimuth.degrees:.2f},{elevation.degrees:.2f}\n"
        if controller:
            try:
                controller.write(msg.encode('utf-8'))
            except Exception as e:
                print(f"Serial write failed: {e}")

init()