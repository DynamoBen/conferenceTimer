import threading
import time

class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 30

    def run(self):
        while self.count > 0 and not self.event.is_set():
            print (self.count)

            if self.count < 155:
                self.setInd(1, 1)			# "Talk"
                self.setInd(2, 0)
                self.setInd(3, 0)	
            elif self.count > 15 and self.count < 30:				
                self.setInd(1, 0)			# "Sum-up"
                self.setInd(2, 1)
                self.setInd(3, 0)
            else:
                self.setInd(1, 0)			# "Stop"
                self.setInd(2, 0)
                self.setInd(3, 1)
                             
            self.count -= 1
            self.event.wait(1)
            
    def stop(self):
        self.event.set()


