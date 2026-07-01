import socket


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    client_sock.connect(address)
    while (text := input()) != "kill":
        client_sock.send(text.encode())
        response = client_sock.recv(1024)
        print(f"Response from server: {response.decode()}")
    client_sock.close()


if __name__ == "__main__":
    client()
