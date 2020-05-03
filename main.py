#!/usr/bin/env python3
import threading
import time
import sys

from RCReceiver import RCReceiver
from CarControl import CarControl
from Camera import Camera

CHANNEL_1 = 0
CHANNEL_2 = 1
channelData = [0.0, 0.0]

# SETUP
receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200)
control = CarControl(steering_zero = 1500,
steering_trim = -1.9,
throttle_zero = 1250,
steering_pin = 18,
throttle_pin = 12)
camera = Camera("Car front")

# INITIALIZE CAR
if not receiver.startListening():
    print('Error opening Port')
    sys.exit()

receiver_thread = threading.Thread(target=receiver.read, args=(channelData,), daemon=True)
receiver_thread.start()

control.start()
camera.startLiveFeed()
# LOOP
try:
    while True:
        print(channelData)
        control.steer(data[CHANNEL_1])
        control.accelerate(data[CHANNEL_2])
# TERMINATE
except KeyboardInterrupt:
    camera.stopLiveFeed()
    control.stop()
    if not receiver.stopListening():
        print('Error closing Port')
