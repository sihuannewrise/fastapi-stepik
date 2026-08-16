import asyncio
import time
from random import randint


async def client(address):
    client_name = f"Клиент_№{randint(1, 100)}"
    for i in range(5_000):
        start_time = time.perf_counter()
        reader, writer = await asyncio.open_connection(*address)
        message = f"{client_name} {i} {i}"
        print(f"{client_name} отправил: {message!r}")
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(1024)
        print(f"{client_name} получил: {data.decode()!r}")
        writer.close()
        await writer.wait_closed()
        print(f"На цикл запрос - ответ было потрачено {time.perf_counter()-start_time:.4f}с.")


if __name__ == "__main__":
    address = ("localhost", 5555)
    asyncio.run(client(address))
