import socket

from evloop.event_loop import EventLoop
from evloop.signal import AddEvent, WaitRecv, WaitSend


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 5150))
        sock.listen()

        while True:
            yield WaitRecv(sock)
            client, _ = sock.accept()
            yield AddEvent(handle_client(client))


def handle_client(sock):
    while True:
        yield WaitRecv(sock)
        data = sock.recv(1024)
        if not data:
            break

        yield WaitSend(sock)
        sock.send(data)
    sock.close()


evloop = EventLoop(debug=True)
evloop.add(start_server())

evloop.loop()
