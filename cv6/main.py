from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self):
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
    while True:
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
        name = "Hacker : %2d" , (hacker_id)
        board(name)
        shared.bar.wait()

        if shared.is_capitan:
            rowBoat(shared)
            shared.mutex.unock()


def serve(serve_id, shared):
    while True:
        shared.mutex.lock()
        shared.serfs += 1
        if shared.serfs == 4:
            shared.is_capitan = True
            shared.serfs -= 4
            shared.servesQ.signal(4)
        elif shared.serfs == 2 and shared.hackers >= 2:
            shared.is_capitan = True
            shared.serfs -= 2
            shared.servesQ.signal(2)
            shared.hackers -= 2
            shared.hackersQ.signal(2)
        else:
            shared.mutex.unlock()
        shared.hackersQ.wait()
        name = "Serve : %2d" , (serve_id)
        board(name)
        shared.bar.wait()

        if shared.is_capitan:
            rowBoat(shared)
            shared.mutex.unock()


def board(name):
    sleep(0.4 + randint(0, 2) / 10)
    print("%2d sa práve nalodil", (name))


def row_boat(shared):
    print("HURAAAAAAAA, VYRÁŽAME!!!!")
    shared.is_capitan = False


