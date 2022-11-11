from evloop.event_loop import EventLoop
from evloop.signal import AddEvent, WaitEvent, WaitSleep


def cr_say_mai():
    while True:
        print('mai')
        yield


def cr_say_mati():
    for _ in range(10):
        print('mati')
        yield


def cr_sleep():
    yield WaitSleep(10)


def cr_main():
    for _ in range(1000):
        yield AddEvent(cr_sleep())


evloop = EventLoop(debug=True)
evloop.add(cr_main())

evloop.loop()
