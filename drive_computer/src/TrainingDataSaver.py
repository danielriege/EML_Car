from concurrent.futures import ThreadPoolExecutor
from queue import Queue 
import cv2

class TrainingDataSaver:
    def __init__(self, threads=5, bufferSize=128, name="test"):
        self.threads = threads
        self.name = name
        self.stopped = False
        self.Q = Queue(maxsize=bufferSize)
    def start(self):
        self.executor = ThreadPoolExecutor(max_workers=self.threads)
        for _ in range(0, self.threads):
            self.executor.submit(self.task)
    def task(self):
        print("[TrainingDataSaver] new thread started")
        while True:
            while self.Q.qsize() < 1:
                if stopped == True:
                    break
            (frame, loopRun, ch1, ch2) = self.Q.get()
            cv2.imwrite("../training_data/%s_%04d_%04d_%04d.jpg" % (self.name,
                                                                    loopRun,
                                                                    ch1, ch2),
                        frame)
    def stop(self):
        self.stopped = True
        self.executor.shutdown(wait=True)
    def add(self, data):
        if not self.Q.full():
            self.Q.put(data)
