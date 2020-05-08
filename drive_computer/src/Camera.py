#!/usr/bin/env python3
import time
from threading import Thread
import cv2
import sys
from queue import Queue

class Camera:
    def __init__(self, queueSize=128):
        self.stream = cv2.VideoCapture(0)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_FPS, 30)
        
        self.stopped = False
	# initialize the queue used to store frames read from
	# the camera
        
        self.Q = Queue(maxsize=queueSize)
    def start(self):
	# start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    def stop(self):
        self.stopped = True
    def update(self):
        while True:
            if self.stopped:
                return
            # ensure the queue has room in it
            if not self.Q.full():
	    # read the next frame from the file
                (grabbed, frame) = self.stream.read()
                if not grabbed:
                    continue
                self.Q.put(frame)
    def read(self):
	# return next frame in the queue
        return self.Q.get()
    def available(self):
        return self.Q.qsize() > 0
if __name__ == "__main__":
    test_camera = Camera()
    print("Starting live preview...")
    # buffers camera stream in a queue on seperate thread
    test_camera.start()
    prevtime = 0
    try:
        while True:
            frame = test_camera.read()
            cv2.putText(frame, "Queue Size: {}".format(test_camera.Q.qsize()),
		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            # simulate neural net interferance
            time.sleep(0.02)
            # wait until buffer has more frames to process
            while not test_camera.available():
                continue
            print((time.time()-prevtime)*1000,"ms")
            prevtime = time.time()
    except KeyboardInterrupt:
        test_camera.stop()
