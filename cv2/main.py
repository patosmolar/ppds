from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print

class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.count += 1
        if self.count == self.n:
            self.count = 0
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()

def uloha_1(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)

barrier = SimpleBarrier(5)

t1 = Thread(uloha_1, barrier, 1)
t2 = Thread(uloha_1, barrier, 2)
t3 = Thread(uloha_1, barrier, 3)
t4 = Thread(uloha_1, barrier, 4)
t5 = Thread(uloha_1, barrier, 5)

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
