import socket
import multiprocessing


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.bind(address)
    server_sock.listen(1)
    conn, addr = server_sock.accept()
    data = conn.recv(1024)
    print(f"Получил данные {data} от клиента с адресом {addr}")
    server_sock.close()


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    client_sock.connect(address)
    message = b"Hello from client!"
    client_sock.send(message)
    client_sock.close()


def main():
    pr_server = multiprocessing.Process(target=server)  # создаем процесс сервер и запускаем
    pr_server.start()

    pr_client = multiprocessing.Process(target=client)  # создаем процесс клиента и запускаем
    pr_client.start()

    pr_server.join()  # ожидаем заверешения работы процесса сервера
    pr_client.join()  # ожидаем заверешения работы процесса клиента


if __name__ == "__main__":
    main()
