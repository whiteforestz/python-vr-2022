import select
import time
from collections import deque

from evloop.event import Event
from evloop.signal import Signal


class EventLoop:
    def __init__(self, *, debug=False):
        self.debug = debug
        self.queue = deque()
        self.events = {}

        self.waiting_event = {}
        self.waiting_sleep = {}
        self.waiting_recv = {}
        self.waiting_send = {}

    def loop(self):
        self.add(self.io())

        while self.events:
            event = self.queue.popleft()

            try:
                msg = event.run()
                if isinstance(msg, Signal):
                    msg.handle(event, self)
                    continue
            except StopIteration:
                self.terminate(event)
                continue

            self.queue.append(event)

    def add(self, cr):
        event = Event(cr)
        self.schedule(event)

        if self.debug:
            print(f'event #{event.eid} added')

        return event.eid

    def schedule(self, event):
        self.events[event.eid] = event
        self.queue.append(event)

    def wait_for_event(self, event, eid):
        if eid not in self.events:
            return False

        self.waiting_event.setdefault(eid, []).append(event)
        return True

    def wait_for_sleep(self, event, secs):
        self.waiting_sleep[event.eid] = (event, time.time() + secs)

    def wait_for_recv(self, event, fd):
        self.waiting_recv[fd] = event

    def wait_for_send(self, event, fd):
        self.waiting_send[fd] = event

    def terminate(self, event):
        del self.events[event.eid]
        for waiting_event in self.waiting_event.pop(event.eid, []):
            self.schedule(waiting_event)

        if self.debug:
            print(f'event #{event.eid} terminated')

    def io(self):
        while True:
            for eid, (event, until) in list(self.waiting_sleep.items()):
                if time.time() >= until:
                    del self.waiting_sleep[eid]
                    self.schedule(event)

            if not self.queue:
                self.select(None)
            else:
                self.select(0)

            yield

    def select(self, timeout):
        if self.waiting_recv or self.waiting_send:
            rd, wr, _ = select.select(self.waiting_recv, self.waiting_send, [], timeout)

            for fd in rd:
                event = self.waiting_recv.pop(fd)
                self.schedule(event)

            for fd in wr:
                event = self.waiting_send.pop(fd)
                self.schedule(event)
