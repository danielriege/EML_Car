#!/usr/bin/env python3
import threading
import time
import sys
import cv2
import glob
import argparse
from queue import Queue
from multiprocessing.dummy import Pool as ThreadPool

from src.RCReceiver import RCReceiver
from src.CarControl import CarControl
from src.Camera import Camera
from src.TrainingDataSaver import TrainingDataSaver
from src.LaneNavigator import LaneNavigator

# DEFINES
CHANNEL_1 = 0
CHANNEL_2 = 1

def main():
    # CONFIGURATION
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mode', type=str, help='Mode to run e.g. [t]raining or [a]utonomous ', required=True)
    parser.add_argument('--name', type=str, help='in manual mode = name of training folder; in autonomous = model name',
                        required=True)
    parser.add_argument('--receiver', type=str, help='Serial port of RCReceiver Arduino unit e.g. /dev/ttyUSB0', required=False,
                        default="/dev/ttyUSB0")
    args = parser.parse_args()
    if args.mode == "t":
        training = True
        print("Running in training mode")
    elif args.mode == "a":
        training = False
        print("Running in autonomous mode")
    else:
        print("Mode unkown")
        return
    run_name = args.name
    serial_port = args.receiver
    # SETUP
    control = CarControl(steering_zero = 1500,
    steering_trim = -1.9,
    throttle_zero = 1250,
    steering_pin = 18,
    throttle_pin = 12)
    control.start()
    camera = Camera(255)
    camera.start()

    # will be called when the receiver has a new value for a channel
    def controlCallback(ch, pwm):
        if ch == CHANNEL_1 and training == True:
            control.steer(pwm)
        if ch == CHANNEL_2:
#            if training == True:
            control.accelerate(pwm)
 #           else:  
  #              control.cruiseControl(pwm)
    receiver = RCReceiver(port=serial_port, baudrate=115200, _callback=controlCallback)
    receiver.start()
    time.sleep(2)
    if training:
        training_data_saver = TrainingDataSaver(threads=7, bufferSize=128, name=run_name)
        training_data_saver.start()
    else:
        lane_navigator = LaneNavigator("./models/%s_edgetpu.tflite" % run_name)

    # LOOP
    try:
        prevtime = time.time()
        period = 100
        loopRun = 0
        while True:
            frame = camera.read()
            if training:
                channelData = receiver.getChannelData()
                training_data_saver.add((frame, loopRun, channelData[CHANNEL_1], channelData[CHANNEL_2]))
#                print("[Receiver] ",channelData)
            else:
                start = time.time()
                steering_angle = lane_navigator.predictSteeringAngle(frame)
#                print('angle:',steering_angle,' interferance took: ', (time.time()-start)*1000, 'ms')
                control.steer(steering_angle)
            # Frame 
            cv2.putText(frame, "Frame Buffer: {}".format(camera.Q.qsize()),
    		(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            fps = int((1/period)*1000)
            cv2.putText(frame, "FPS: %d" % fps, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2)
            if training:
                steering_angle = channelData[CHANNEL_2]
            cv2.putText(frame, "Steering: %d" % steering_angle, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            # wait until buffer has more frames to process
            while not camera.available():
                continue
            period = (time.time()-prevtime)*1000
#            print("loop period: ",period,"ms")
            prevtime = time.time()
            loopRun += 1
    except KeyboardInterrupt:
        control.stop()
        receiver.stop()
        receiver.join()
        camera.stop()
        if training:
            training_data_saver.stop()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
