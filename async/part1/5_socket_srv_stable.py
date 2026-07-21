import socket
import math

def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()
    while True:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")  # логируем подключение
        while data := conn.recv(1024):  # получаем и обрабатываем запросы
            print(f"received data {data}")
            try:
                numbers = [int(n) for n in data.decode().split()]
                res = math.prod(numbers)
            except Exception as er:
                msg = repr(er)
            else:
                msg = f'{"*".join(map(str, numbers))}={res}'
            finally:
                conn.send(msg.encode())

if __name__ == "__main__":
    server()