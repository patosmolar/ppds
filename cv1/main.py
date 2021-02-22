from fei.ppds import Thread
from fei.ppds import Mutex


class Shared:

    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):

    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def fnc1(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


def fnc2(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            break
        shared.array[shared.counter] += 1
        shared.mutex.unlock()
        shared.counter += 1


def fnc3(shared):
    while shared.counter < shared.end:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(10):
    sh = Shared(1000000)
    t1 = Thread(fnc3, sh)
    t2 = Thread(fnc3, sh)

    t1.join()
    t2.join()

    print Histogram(sh.array)
