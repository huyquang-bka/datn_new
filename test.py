from threading import Thread
import time

import cv2

stop_thread = False

class SomeThread(Thread):
    def __init__(self):
        super().__init__()
        self.__is_active = False
    
    def run(self):
        cap = cv2.VideoCapture(0)
        self.__is_active = True
        while self.__is_active:
            print(time.time())
            ret, frame = cap.read()
            time.sleep(1)
            if stop_thread:
                break
        cap.release()
        self.stop()
    
    def stop(self):
        self.__is_active = False
        
        
def stop():
    global stop_thread
    stop_thread = True

t1 = SomeThread()
t2 = Thread(target=stop)

t1.start()
time.sleep(7)
t2.start()
t2.join()