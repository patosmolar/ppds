from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex,Event, print


class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)
        self.event = Event()

    def wait_with_semaphore(self):
        self.mutex.lock()
        self.count += 1
        if self.count == self.n:
            self.count = 0
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()

    def wait_with_events(self):
        self.mutex.lock()
        if(self.count == 0):
            self.event.clear()
        self.count += 1
        if self.count == self.n:
            self.count = 0
            self.event.signal()   
        self.mutex.unlock()
        self.event.wait()


def uloha_1(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    #barrier.wait_with_semaphore
    barrier.wait_with_events()
    print("vlakno %d po bariere" % thread_id)

def rendezvous(thread_name):
    sleep(randint(1,10)/10)
    print('rendezvous: %s' % thread_name)
 
 
def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1,10)/10)
 
 
def uloha_2(b1,b2,thread_name):
    """Kazde vlakno vykonava kod funkcie 'barrier_example'.
    Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    nielen pred vykonanim funkcie 'ko', ale aj
    *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
    """
 
    while True:
        rendezvous(thread_name)
        b1.wait_with_events()
        ko(thread_name)
        b1.wait_with_events()
 
 


barr1 = SimpleBarrier(5)
barr2 = SimpleBarrier(5)

threads = list()
for i in range(5):
    t = Thread(uloha_2, barr1,barr2, f'Thread {i}')
    threads.append(t)
 
for t in threads:
    t.join()
