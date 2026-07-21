import select
import socket
from collections import deque


def server():
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()
    while True:
        yield "accept", server_sock
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        tasks.append(client(conn))


def client(client_sock: socket.socket):
    while True:
        yield "recv", client_sock
        data = client_sock.recv(1024)
        print(f"received data {data}")
        try:
            numbers = [int(n) for n in data.decode().split()]
            res = sum(numbers)
        except Exception as er:
            msg = repr(er)
        else:
            msg = f'{"+".join(map(str, numbers))}={res}'
        finally:
            yield "send", client_sock
            client_sock.send(msg.encode())


def event_loop():
    for_read = {}
    for_write = {}
    while True:
        if not tasks:
            sockets_for_read, sockets_for_write, _ = select.select(for_read, for_write, [])
            for sock in sockets_for_read:
                tasks.append(for_read.pop(sock))
            for sock in sockets_for_write:
                tasks.append(for_write.pop(sock))

        task = tasks.popleft()
        try:
            method, conn = next(task)
            if method == "send":
                for_write[conn] = task
            else:
                for_read[conn] = task
        except socket.error as error:
            print(error)


if __name__ == "__main__":
    tasks = deque((server(),))
    event_loop()
