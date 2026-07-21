import socket


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.bind(address)
    server_sock.listen(1)

    conn, addr = server_sock.accept()
    data = conn.recv(1024)
    print(f"Сервер получил данные {data} от клиента с адресом {addr}")

    number = int.from_bytes(data)
    quadro = number**2
    print(f"Квадрат числа {number} равен {quadro}")

    # message = b"Hello from server!"
    # print("и отправил ответ")
    conn.send(quadro.to_bytes(16))

    server_sock.close()


if __name__ == "__main__":
    server()
