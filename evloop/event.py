class Event:
    global_eid = 0

    def __init__(self, cr):
        Event.global_eid += 1

        self.eid = Event.global_eid
        self.cr = cr
        self.buf = None

    def run(self):
        msg = self.cr.send(self.buf)
        self.buf = None
        return msg
