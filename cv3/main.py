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
        self.turniket = Semaphore(1)


def read_write():
    rd_ls = LightSwitch()
    sh = Shared()

    n_writers = 1
    n_readers = 5
    t_read = 10
    t_write = 50
    n_repeats = 10

    def read(read_ls, shared):
        for _ in range(n_repeats):
            # shared.turniket.wait()
            # shared.turniket.signal()
            print("before read")
            read_ls.lock(shared.semaphore)
            print("inside read")
            sleep(randint(1, 10) / t_read)
            read_ls.unlock(shared.semaphore)
            print("outside read")

    def write(shared):
        for _ in range(n_repeats):
            # shared.turniket.wait()
            print("before of write")
            shared.semaphore.wait()
            sleep(randint(1, 10) / t_write)
            print("inside write")
            # shared.turniket.signal()
            shared.semaphore.signal()
            print("outside write")

    threads = []

    for _ in range(n_readers):
        t = Thread(read, rd_ls, sh)
        threads.append(t)
    for _ in range(n_writers):
        t = Thread(write, sh)
        threads.append(t)
    for t in threads:
        t.join()

read_write()
