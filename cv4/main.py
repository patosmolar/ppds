from fei.ppds import Mutex, Semaphore, Thread, print, Event
from time import sleep
from random import randint


class LightSwitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        counter = self.counter
        self.counter = 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Elektraren(object):
    def __init__(self):
        self.ls_monitor = LightSwitch()
        self.ls_sensor = LightSwitch()
        self.monitor_acess = Semaphore(1)
        self.sensor_acess = Semaphore(1)

    def monitor(self, monitor_id):
        while True:
            self.monitor_acess.wait()
            n_monitors_reading = self.ls_monitor.lock(self.sensor_acess)
            self.monitor_acess.signal()
            read_time = randint(40, 50) / 1000
            print(
                'monit "d": pocet_citajucich_monitorov=d, trvanie_citania=f\n'
                % (monitor_id, n_monitors_reading, read_time)
            )
            sleep(read_time)
            self.monitor_ls.unlock(self.no_sensor)