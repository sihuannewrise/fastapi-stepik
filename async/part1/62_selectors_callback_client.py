import socket
from time import sleep


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    client_sock.connect(address)
    for i in range(1_00):
        sleep(0.1)
        client_sock.send(f"{i} {i}".encode())
        response = client_sock.recv(1024)
        print(f"Response from server: {response.decode()}")
    client_sock.close()


if __name__ == "__main__":
    client()
