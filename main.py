import tracker
import serial
import time
from tracker import az, alt


controller = serial.Serial('COM3', 9600)

def init():
    tracker.init()

def main():
    while True:
        msg = f"{az.degrees:.2f},{alt.degrees:.2f}\n"
        controller.write(msg.encode('utf-8'))

init()