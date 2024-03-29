from queue import Queue
from threading import Thread
import cv2

class TrainingDataSaver:
    def __init__(self, name, threads=5, bufferSize=128):
        self.threads = threads
        self.name = name
        self.stopped = False
        self.Q = Queue(maxsize=bufferSize)
        self.threadList = []
    def start(self):
        print("[TrainingDataSaver] starting threads: ",self.threads)
        for _ in range(0, self.threads):
            t = Thread(target=self.task)
            t.start()
            self.threadList.append(t)
    def task(self):
        print("[TrainingDataSaver] new thread started.")
        while not self.stopped:
            (frame, loopRun, ch1, ch2) = self.Q.get()
            cv2.imwrite("./training_data/%s/%05d_%04d_%04d.jpg" % (self.name,loopRun,ch1, ch2),frame)
        print("[TrainingDataSaver] one thread stopped.")
    def stop(self):
        print("[TrainingDataSaver] stopping all threads...")
        self.stopped = True
        for thread in self.threadList:
            thread.join()
        self.threads = []
        print("[TrainingDataSaver] all threads stopped.")
    def add(self, data):
        if not self.Q.full():
            self.Q.put(data)
