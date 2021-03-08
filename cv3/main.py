from fei.ppds import Mutex, Semaphore, Thread, print
from time import sleep
from random import randint


class LightSwitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared(object):
    def __init__(self):
        self.semaphore = Semaphore(1)


def read_write():
    rd_ls = LightSwitch()
    sh = Shared()

    def read(read_ls, shared):
        while True:   
            print("before read")
            read_ls.lock(shared.semaphore)
            print("inside read")
            sleep(randint(1,10)/10)
            read_ls.unlock(shared.semaphore)
            print("outside read")

    def write(shared):
        while True:   
            print("before of write")
            shared.semaphore.wait()
            sleep(randint(1,10)/10)
            print("inside write")
            shared.semaphore.signal()
            print("outside write")

    threads= []

    for _ in range(5):
        t = Thread(read,rd_ls,sh)
        threads.append(t)
    for _ in range(1):
        t = Thread(write,sh)
        threads.append(t)
    for t in threads:
        t.join()

read_write()
