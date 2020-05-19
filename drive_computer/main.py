#!/usr/bin/env python3
import threading
import time
import sys
import cv2
import glob
from queue import Queue
from multiprocessing.dummy import Pool as ThreadPool

from src.RCReceiver import RCReceiver
from src.CarControl import CarControl
from src.Camera import Camera
from src.TrainingDataSaver import TrainingDataSaver
from src.LaneNavigator import LaneNavigator


CHANNEL_1 = 0
CHANNEL_2 = 1

prevtime = time.time()
test_run_name = "test1"
if len(sys.argv) > 1:
    test_run_name = sys.argv[1]

# SETUP
print("[Control] starting...")
control = CarControl(steering_zero = 1500,
steering_trim = -1.9,
throttle_zero = 1250,
steering_pin = 18,
throttle_pin = 12)
control.start()
print("[Camera] starting...")
camera = Camera(255)
camera.start()
lane_navigator = LaneNavigator("../CNN/black_dot_edgetpu.tflite")

# will be called when the receiver has a new value for a channel
def controlCallback(ch, pwm):
    #if ch == CHANNEL_1:
        #control.steer(pwm)
    if ch == CHANNEL_2:
        control.accelerate(pwm)
receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200, _callback=controlCallback)
print("[Receiver] starting...")
receiver.start()
print("[Receiver] waiting for connection...")
time.sleep(2)
print("[Receiver] ready")
#print("starting thread pool...")
#training_data_saver = TrainingDataSaver(threads=7, bufferSize=128, name=test_run_name)
#training_data_saver.start()



print("starting control loop...")
# LOOP
try:
    loopRun = 0
    while True:
        frame = camera.read()
        #channelData = receiver.getChannelData()

        #training_data_saver.add((frame, loopRun, channelData[CHANNEL_1],
        #                         channelData[CHANNEL_2]))
        start = time.time()
        steering_angle = lane_navigator.predictSteeringAngle(frame)
        print('angle:',steering_angle,' interferance took: ', (time.time()-start)*1000, 'ms')
        control.steer(steering_angle)

        cv2.putText(frame, "Frame Buffer: {}".format(camera.Q.qsize()),
		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        #print("[Receiver] ",channelData)

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        # wait until buffer has more frames to process
        while not camera.available():
            continue
        #print("[Camera] period: ",(time.time()-prevtime)*1000,"ms")
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
    #print("[TrainingDataSaver] stopping...")
    #training_data_saver.stop()
    cv2.destroyAllWindows()
    print("All units stopped")
