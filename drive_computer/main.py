#!/usr/bin/env python3
import threading
import time
import sys
import cv2
import glob

from src.RCReceiver import RCReceiver
from src.CarControl import CarControl
from src.Camera import Camera


CHANNEL_1 = 0
CHANNEL_2 = 1

prevtime = time.time()
channelData = [0.0, 0.0]
test_run_name = "test1"

# SETUP
receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200)
control = CarControl(steering_zero = 1500,
steering_trim = -1.9,
throttle_zero = 1250,
steering_pin = 18,
throttle_pin = 12)
camera = Camera()

# INITIALIZE CAR
print("[Receiver] starting...")
receiver.start()
print("[Receiver] waiting for connection...")
time.sleep(2)
print("[Receiver] ready")
print("[Control] starting...")
control.start()
print("[Camera] starting...")
camera.start()
print("starting control loop...")
# LOOP
try:
    loopRun = 0
    while True:
        frame = camera.read()

        channelData = receiver.getChannelData()
        print("[Receiver] ",channelData)
        control.steer(channelData[CHANNEL_1])
        control.accelerate(channelData[CHANNEL_2])

        cv2.imshow("Frame", image)
        cv2.imwrite("../training_data/%s_%04d_%04d_%04d.jpg" % (test_run_name, loopRun, channelData[CHANNEL_1], channelData[CHANNEL_2]), image)
        # wait until buffer has more frames to process
        while not camera.available():
        print("[Camera] period: ",(time.time()-prevtime)*1000,"ms")
        prevtime = time.time()
        loopRun += 1
except KeyboardInterrupt:
    print("[Control] stopping the car")
    control.stop()
    print("[Receiver] signaling thread to stop")
    receiver.stop()
    print("[Receiver] waiting for teardown")
    receiver.join()
    print("[Receiver] thread killed sucessfully")
    print("[Camera] signaling thread to stop")
    camera.stop()
    cv2.destroyAllWindows()
    print("All units stopped")
