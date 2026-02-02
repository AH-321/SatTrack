import tracker
import serial
import time
import gui

#controller = serial.Serial('COM3', 9600)

def init():
    gui.init()

def main():
    while True:

        azimuth, elevation, distance, sat_name = tracker.fetch()

        msg = f"{azimuth.degrees:.2f},{elevation.degrees:.2f}\n"
        #controller.write(msg.encode('utf-8'))

init()