import socket
import selectors
from typing import Tuple


def create_server(address: Tuple[str, int]) -> socket.socket:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen()
    return server_socket


def handler(data: bytes) -> bytes:
    try:
        print(f"received data {data}")
        numbers = [int(n) for n in data.decode().split()]
        res = sum(numbers)
    except Exception as er:
        msg = repr(er)
    else:
        msg = f'{"+".join(map(str, numbers))}={res}'
    finally:
        return msg.encode()


def accept_conn(server_sock: socket.socket, sel: selectors.BaseSelector) -> None:
    try:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        sel.register(conn, selectors.EVENT_READ, send_response)
    except socket.error as e:
        print(f"Error accepting connection: {e}")


def send_response(client_sock: socket.socket, *args) -> None:
    data = client_sock.recv(1024)
    response = handler(data)
    client_sock.send(response)


def event_loop(server_socket: socket.socket) -> None:
    with selectors.DefaultSelector() as sel:
        sel.register(server_socket, selectors.EVENT_READ, accept_conn)
        while True:
            for k, _ in sel.select():
                sock: socket.socket = k.fileobj
                callback = k.data  # обращаемся к ассоциированной функции через .data
                try:
                    callback(sock, sel)  # вызываем коллбэк
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    sock.close()
                    sel.unregister(sock)


if __name__ == "__main__":
    address = ("localhost", 5555)
    server_socket = create_server(address)
    event_loop(server_socket)
