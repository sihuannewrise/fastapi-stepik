import socket
from time import perf_counter, sleep
from random import randint, uniform
from multiprocessing import Process


def generate_numbers() -> str:
    numbers = [str(randint(1, 100)) for _ in range(randint(2, 5))]
    return ' '.join(numbers)

def launch_client(client_id: int, count_requests: int | None = None) -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    try:
        start_connect = perf_counter()
        client_sock.connect(address)
        connect_time = perf_counter() - start_connect
        print(f'Клиент {client_id} подключился за {connect_time:.4f} с')

        for i in range(count_requests):
            data = generate_numbers() # Генерируем данные
            start_time = perf_counter() # Замеряем время запроса
            client_sock.send(data.encode()) # Отправка запроса
            response = client_sock.recv(4096) # Ответ от сервера
            request_time = perf_counter() - start_time # Время на запрос

            print(f"Клиент {client_id}, запрос {i + 1}: "
                  f"отправил '{data}', получил '{response.decode()}', "
                  f"время = {request_time:.6f} сек")

            sleep(uniform(0.2, 0.5))

    except Exception as err:
        print(f"Клиент {client_id}: ошибка - {err}")

    finally:
        client_sock.close()


def run_multiple_clients(num_clients: int, requests_per_client: int | None = None) -> None:
    """Запуск нескольких клиентов в отдельных процессах"""
    print(f'Запуск {num_clients} клиентов')

    start_time = perf_counter()

    processes = []
    for i in range(num_clients):
        process = Process(target=launch_client, args=(i + 1, requests_per_client))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'Все клиенты завершили работу за {perf_counter() - start_time:.3f} с')


if __name__ == '__main__':
    for num in [2, 5, 7, 10]:
        run_multiple_clients(num, 5)
        print("\n" + "-" * 50 + "\n")
