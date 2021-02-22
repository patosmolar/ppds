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

            
def fnc(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.array[shared.counter] += 1
        shared.counter += 1



for _ in range(10):
    sh = Shared(1000000)
    t1 = Thread(fnc, sh)
    t2 = Thread(fnc, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array)) 
