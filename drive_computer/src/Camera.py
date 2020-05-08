#!/usr/bin/env python3
import time
import threading
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
				grabbed, frame = self.stream.read()
                if not grabbed:
                    continue
				self.Q.put(frame)
    def read(self):
		# return next frame in the queue
		return self.Q.get()
    def available(self):
		return self.Q.qsize() > 0
if __name__ == "__main__":
    def teardown():
        cv2.destroyAllWindows()
    prevtime = 0
    def callback(image, loopRun):
        global prevtime
        cv2.imshow("Frame", image)
        print((time.time()-prevtime)*1000,"ms")
        prevtime = time.time()


    test_camera = Camera()
    print("Starting live preview...")
    # buffers camera stream in a queue on seperate thread
    test_camera.start()
    prevtime = 0
    try:
        while True:
            frame = test_camera.read()

            cv2.imshow("Frame", frame)
            # simulate neural net interferance
            time.sleep(0.02)
            # wait until buffer has more frames to process
            while not test_camera.available():
            print((time.time()-prevtime)*1000,"ms")
            prevtime = time.time()
    except KeyboardInterrupt:
        test_camera.stop()
