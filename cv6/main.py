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
        self.hackersQ = Semaphore(0)
        self.servesQ = Semaphore(0)
        self.bar = SimpleBarrier(4)


def hacker(hacker_id, shared):
    while True:
        # inicializácia lokálnej premennej
        is_capitan = False

        # init mena pre výpis do funkcie
        name = "Hacker : %2d" % hacker_id

        # začiatok KO
        shared.mutex.lock()
        shared.hackers += 1

        # prvá podmienka pre vyplávanie
        if shared.hackers == 4:
            # posledné vlákno je teda kapitán
            is_capitan = True
            print("%s sa stal Kapitánom! HIP-HIP-HURAAA" % name)
            # vynuluje počítadlo
            shared.hackers -= 4
            # pustí 3 čakajúcich + seba
            shared.hackersQ.signal(4)

        # alternatívna podmienka pre vyplávanie
        elif shared.hackers == 2 and shared.serfs >= 2:
            # o5 je posledný kapitán
            is_capitan = True
            print("%s sa stal Kapitánom! HIP-HIP-HURAAA" % name)
            # vynuluje a pustí jedného + seba
            shared.hackers -= 2
            shared.hackersQ.signal(2)
            # vynuluje a pustí dvoch čakajúcich serfs
            shared.serfs -= 2
            shared.servesQ.signal(2)
        else:
            # ak nie su splnené podmienky, čaká a pustí dalšieho do KO
            shared.mutex.unlock()

        print("%s čaká na nalodenie" % name)

        # tu čakajú kým nebude splnená hociaká podmienka
        shared.hackersQ.wait()

        # simulacia nalodenia
        board(name)
        # tu sa pekne počkáme kým nebudeme 4
        shared.bar.wait()

        # kapitán naštartuje loď + uvolní svoj mutex
        if is_capitan:
            row_boat()
            shared.mutex.unlock()


# to isté ako hacker, iba opačne
def serve(serve_id, shared):
    while True:
        is_capitan = False
        name = "Serve : %2d" % serve_id
        shared.mutex.lock()
        shared.serfs += 1
        if shared.serfs == 4:
            is_capitan = True
            print("%s sa stal Kapitánom! HIP-HIP-HURAAA" % name)
            shared.serfs -= 4
            shared.servesQ.signal(4)
        elif shared.serfs == 2 and shared.hackers >= 2:
            is_capitan = True
            print("%s sa stal Kapitánom! HIP-HIP-HURAAA" % name)
            shared.serfs -= 2
            shared.servesQ.signal(2)
            shared.hackers -= 2
            shared.hackersQ.signal(2)
        else:
            shared.mutex.unlock()

        print("%s čaká na nalodenie" % name)
        shared.servesQ.wait()

        board(name)
        shared.bar.wait()

        if is_capitan:
            row_boat()
            shared.mutex.unlock()


# simulácia nalodenia, name = meno nastupujucého
def board(name):
    sleep(0.4 + randint(0, 2) / 10)
    print("%s sa práve nalodil" % name)


# štart lode
def row_boat():
    print("HURAAAAAAAA, VYRÁŽAME!!!!")
    sleep(1 + randint(0, 2))


def init_and_run():
    """Spustenie modelu"""
    threads = list()
    shared = Shared()

    for hacker_id in range(0, 4):
        threads.append(Thread(hacker, hacker_id, shared))

    for serve_id in range(0, 4):
        threads.append(Thread(serve, serve_id, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run()
