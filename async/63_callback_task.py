import socket
import selectors


def accept_conn(server_sock: socket.socket, sel: selectors.BaseSelector) -> None:
    try:
        conn, addr = server_sock.accept()
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
            events = sel.select(2)
            if not events:
                print("Нет новых запросов за отведенный таймаут. Завершаем event_loop.")
                break
            for key, _ in events:
                sock: socket.socket = key.fileobj
                callback = key.data
                try:
                    callback(sock, sel)
                except socket.error as e:
                    print("Потеря связи с клиентом. Закрываем сокет, снимаем с регистрации.")
                    sock.close()
                    sel.unregister(sock)
