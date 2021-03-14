from fei.ppds import Mutex, Semaphore, Thread, print, Event
from time import sleep
from random import randint


class LightSwitch():
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        count = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return count

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class SimpleBarrier:
    def __init__(self, n):
        self.number_to_block = n
        self.count = 0
        self.mutex = Mutex()        
        self.event = Event()
    
    def wait_with_events(self):
        self.mutex.lock()        
        self.count += 1
        if self.count == self.number_to_block:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


class PowerPlant():
    def __init__(self):
        self.ls_monitor = LightSwitch()
        self.ls_sensor = LightSwitch()
        self.monitor_acess = Semaphore(1)
        self.sensor_acess = Semaphore(1)
        self.barrier = SimpleBarrier(3)

    def monitor(self, monitor_id):
        while True:
            self.barrier.event.wait()
            self.monitor_acess.wait()
            n_monitors_reading = self.ls_monitor.lock(self.sensor_acess)
            self.monitor_acess.signal()
            read_time = randint(40, 50) / 1000
            print(
                'monit "%02d": pocet_citajucich_monitorov=%02d, '
                'trvanie_citania=%03f\n'
                % (monitor_id, n_monitors_reading, read_time)
            )
            sleep(read_time)
            self.ls_monitor.unlock(self.sensor_acess)

    def sensor(self, sensor_id, actualisation_time):
        while True:
            sleep(randint(50, 60) / 1000)
            n_sensors_writing = self.ls_sensor.lock(self.monitor_acess)
            self.sensor_acess.wait()
            print(
                'cidlo "%02d": pocet_zapisujucich_cidiel=%02d, '
                'trvanie_zapisu=%03f\n'
                % (sensor_id, n_sensors_writing, actualisation_time)
            )
            sleep(actualisation_time)

            self.sensor_acess.signal()
            self.barrier.wait_with_events()
            self.ls_sensor.unlock(self.monitor_acess)


p = PowerPlant()
threads = []
for i in range(2):
    sensor_pt_time = randint(10, 20) / 1000
    t = Thread(p.sensor, i, sensor_pt_time)
    threads.append(t)

for i in range(1):
    sensor_h_time = randint(20, 25) / 1000
    t = Thread(p.sensor, i + 2, sensor_h_time)
    threads.append(t)

for i in range(8):
    t = Thread(p.monitor, i)
    threads.append(t)

for t in threads:
    t.join()
