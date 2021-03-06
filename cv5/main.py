from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


M = 3
N = 3
# 'C' - number of cooks
C = 2


class SimpleBarrier:
    """Vlastna implementacia bariery
    kvoli specialnym vypisom vo funkcii wait().
    """

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()

    def cooks_wait(self,
                   cook_id,
                   shared):
        self.mutex.lock()
        self.cnt += 1
        print("kuchar %2d úspešne dokončil svoju časť" % (cook_id))
        if self.cnt == self.N:
            self.cnt = 0
            shared.servings += M
            print("kuchar %2d úspešne pridal porciu do hrnca" % (cook_id))
            self.sem.signal(self.N)
            shared.full_pot.signal()
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    """V tomto pripade musime pouzit zdielanu strukturu.
    Kedze Python struktury nema, pouzijeme triedu bez vlastnych metod.
    Preco musime pouzit strukturu? Lebo chceme zdielat hodnotu
    pocitadla servings, a to jednoduchsie v Pythone asi neurobime.
    Okrem toho je rozumne mat vsetky synchronizacne objekty spolu.
    Pri zmene nemusime upravovat API kazdej funkcie zvlast.
    """

    def __init__(self):
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.cooks_barier = SimpleBarrier(C)


def get_serving_from_pot(savage_id, shared):
    """Pristupujeme ku zdielanej premennej.
    Funkcia je volana pri zamknutom mutexe, preto netreba
    riesit serializaciu v ramci samotnej funkcie.
    """

    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        """Pred kazdou hostinou sa divosi musia pockat.
        Kedze mame kod vlakna (divocha) v cykle, musime pouzit dve
        jednoduche bariery za sebou alebo jednu zlozenu, ale kvoli
        prehladnosti vypisov sme sa rozhodli pre toto riesenie.
        """

        shared.barrier1.wait(
            "divoch %2d: prisiel som na veceru, uz nas je %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                             savage_id,
                             print_last_thread=True)

        # Nasleduje klasicke riesenie problemu hodujucich divochov.
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)


def prepare_part_of_meal(id):
    """M je pocet porcii, ktore vklada kuchar do hrnca.
    Hrniec je reprezentovany zdielanou premennou servings.
    Ta udrziava informaciu o tom, kolko porcii je v hrnci k dispozicii.
    """
    print("kuchar %2d: pripravuje svoju časť" % (id))
    # navarenie jedla tiez cosi trva...
    sleep(0.4 + randint(0, 2) / 10)


def cook(M, shared, cook_id):
    """Na strane kuchara netreba robit ziadne modifikacie kodu.
    Riesenie je standardne podla prednasky.
    Navyse je iba argument M, ktorym explicitne hovorime, kolko porcii
    ktory kuchar vari.
    Kedze v nasom modeli mame iba jedneho kuchara, ten navari vsetky
    potrebne porcie a vlozi ich do hrnca.
    """

    while True:
        shared.empty_pot.wait()
        prepare_part_of_meal(cook_id)
        shared.cooks_barier.cooks_wait(cook_id, shared)


def init_and_run(N, M):
    """Spustenie modelu"""
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared))

    for cook_id in range(0, C):
        threads.append(Thread(cook, M, shared, cook_id))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M)
