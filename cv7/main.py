class Scheduler:

    def __init__(self):
        self.list = []
        self.counter = 0

    # schedule at the end of list
    def schedule(self, task):
        self.list.append(task)

    # schedule at start of list
    def schedule_high_priority(self, task):
        self.list.insert(0, task)

    # main loop
    def start_loop(self):
        while self.list:
            self.counter += 1
            task = self.list.pop(0)
            try:
                task.send(self.counter)
                if self.counter % 3 == 0:
                    self.schedule_high_priority(task)
                else:
                    self.schedule(task)
            except StopIteration:
                pass


def cor(m_id):
    mid = m_id
    for a in range(50):
        val = (yield)
        print("id :%d vypisuje hodnotu %d" % (mid,  val))


if __name__ == "__main__":
    s = Scheduler()
    for id in range(1, 10):
        t = cor(id)
        t.send(None)
        s.schedule(t)
    s.start_loop()
