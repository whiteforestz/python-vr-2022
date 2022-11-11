class Signal:
    def handle(self, event, evloop):
        raise NotImplemented


class AddEvent(Signal):
    def __init__(self, cr):
        self.cr = cr

    def handle(self, event, evloop):
        eid = evloop.add(self.cr)
        event.buf = eid
        evloop.schedule(event)


class WaitEvent(Signal):
    def __init__(self, eid):
        self.eid = eid

    def handle(self, event, evloop):
        is_waiting = evloop.wait_for_event(event, self.eid)
        event.buf = is_waiting
        if not is_waiting:
            evloop.schedule(event)


class WaitSleep(Signal):
    def __init__(self, secs):
        self.secs = secs

    def handle(self, event, evloop):
        evloop.wait_for_sleep(event, self.secs)


class WaitRecv(Signal):
    def __init__(self, f):
        self.f = f

    def handle(self, event, evloop):
        fd = self.f.fileno()
        evloop.wait_for_recv(event, fd)


class WaitSend(Signal):
    def __init__(self, f):
        self.f = f

    def handle(self, event, evloop):
        fd = self.f.fileno()
        evloop.wait_for_send(event, fd)
