import socket

from evloop.event_loop import EventLoop
from evloop.signal import WaitSleep, WaitSend, WaitRecv


def start_client(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('0.0.0.0', 5150))

        while True:
            yield WaitSend(sock)
            sock.sendall(msg)

            yield WaitRecv(sock)
            data = sock.recv(1024)

            print(f'received "{data}"')
            yield WaitSleep(0.1)


evloop = EventLoop(debug=True)
evloop.add(start_client(b'Python is awesome!'))
evloop.add(start_client(b'Python not is awesome!'))

evloop.loop()
