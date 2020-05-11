from queue import Queue 
from threading import Thread,Lock
import cv2

mutex = Lock()

class TrainingDataSaver:
    def __init__(self, name, threads=5, bufferSize=128):
        self.threads = threads
        self.name = name
        self.stopped = False
        self.Q = Queue(maxsize=bufferSize)
        self.threadList = []
    def start(self):
        for _ in range(0, self.threads):
            t = Thread(target=self.task)
            t.start()
            self.threadList.append(t)
    def task(self):
        print("[TrainingDataSaver] new thread started")
        while True:
            (frame, loopRun, ch1, ch2) = self.Q.get()
            cv2.imwrite("../training_data/%s/%04d_%04d_%04d.jpg" % (self.name,loopRun,ch1, ch2),frame)
            if self.stopped == True:
                break
    def stop(self):
        self.stopped = True
        for thread in self.threadList:
            thread.join()
        self.threads = []
    def add(self, data):
        if not self.Q.full():
            self.Q.put(data)
