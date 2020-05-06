#!/usr/bin/env python3
import threading
import time
import sys
import cv2
import glob

from RCReceiver import RCReceiver
from CarControl import CarControl
from Camera import Camera


CHANNEL_1 = 0
CHANNEL_2 = 1

prevtime = time.time()
channelData = [0.0, 0.0]
test_run_name = "test1"

# camera will call the loop function every time it gets a picture
def loop(image, loopRun):
    global prevtime
    cv2.imshow("Frame", image)
    cv2.imwrite("training_data/%s_%04d_%04d_%04d.jpg" % (test_run_name, loopRun, channelData[CHANNEL_1], channelData[CHANNEL_2]), image)
    print("[Camera] period: ",(time.time()-prevtime)*1000,"ms")
    prevtime = time.time()
# camera will call teardown when q is pressed
def teardown():
    cv2.destroyAllWindows()

def createVideoFromStream():
    img_array = []
    size = (0,0)
    for filename in sorted(glob.glob("./training_data/*.jpg")):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter("./training_videos/%s.avi" % (test_run_name),
                          cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

# SETUP
receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200)
control = CarControl(steering_zero = 1500,
steering_trim = -1.9,
throttle_zero = 1250,
steering_pin = 18,
throttle_pin = 12)
camera = Camera(loop, teardown)

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
    while True:
        channelData = receiver.getChannelData()
        print("[Receiver] ",channelData)
        control.steer(channelData[CHANNEL_1])
        control.accelerate(channelData[CHANNEL_2])
        time.sleep(0.02)
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
    print("[Camera] waiting for teardown")
    camera.join()
    print("[Camera] thread killed sucessfully")
    print("All units stopped")
    print("generating video from gathered training data")
    createVideoFromStream()
    print("video is saved as:",test_run_name,".avi")
