from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             savage_id):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.hackers = 0
        self.serfs = 0
        self.is_capitan = False
        self.hackersQ = Semaphore(0)
        self.servesQ = Semaphore(0)
        self.bar = SimpleBarrier(4)


def hacker(hacker_id, shared):
    shared.mutex.lock()
    shared.hackers += 1
    if shared.hackers == 4:
        shared.is_capitan = True
        shared.hackers -= 4
        shared.hackersQ.signal(4)
    elif shared.hackers == 2 and shared.serfs >= 2:
        shared.is_capitan = True
        shared.hackers -= 2
        shared.hackersQ.signal(2)
        shared.serfs -= 2
        shared.servesQ.signal(2)
    else:
        shared.mutex.unlock()
    shared.hackersQ.wait()
    board()
    shared.bar.wait()

    if shared.is_capitan:
        rowBoat()
        shared.mutex.unock()
