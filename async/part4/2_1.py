import socket
import select
from collections import deque

# address будет определен в тестовой системе глобально

def server() -> None:
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.setblocking(False)
    server_sock.bind(address)
    server_sock.listen(5)

    tasks = deque()

    def accept_connections():
        while True:
            try:
                conn, addr = server_sock.accept()
                conn.setblocking(False)
                yield conn
            except BlockingIOError:
                yield None

    def handle_client(conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print("Потеря связи с клиентом")
                    break
                try:
                    numbers = [int(n) for n in data.decode().split()]
                    res = sum(numbers)
                    msg = f'{"+".join(map(str, numbers))}={res}'
                except Exception as er:
                    msg = repr(er)
                conn.send(msg.encode())
                yield
            except socket.error:
                print("Потеря связи с клиентом")
                break
            except BlockingIOError:
                yield

    accept_gen = accept_connections()
    tasks.append(('accept', accept_gen))

    while tasks:
        task_type, task_obj = tasks.popleft()

        if task_type == 'accept':
            try:
                conn = next(task_obj)
                if conn is not None:
                    client_gen = handle_client(conn)
                    tasks.append(('client', client_gen))
                tasks.append(('accept', task_obj))
            except StopIteration:
                pass
            except socket.error:
                tasks.append(('accept', task_obj))

        elif task_type == 'client':
            try:
                next(task_obj)
                tasks.append(('client', task_obj))
            except StopIteration:
                pass
            except socket.error:
                print("Потеря связи с клиентом")

def event_loop() -> None:
    server()