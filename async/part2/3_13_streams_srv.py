import asyncio
import time


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    start_time = time.perf_counter()
    try:
        data = await reader.read(1024)
        data = data.decode()
        client_name, *data_numbers = data.split()
        print(f"Получил числа от {client_name}: {data_numbers}")
        numbers = [int(n) for n in data_numbers]
        res = sum(numbers)
    except Exception as er:
        msg = f"{er!r}"
    else:
        msg = f'{"+".join(map(str, numbers))}={res}'
    finally:
        writer.write(msg.encode())
        await writer.drain()
        print(f"Отправил ответ: {msg}")
        writer.close()
        await writer.wait_closed()
        print(f"Клиентский запрос был обработан за {time.perf_counter()-start_time:.4f}с.")


async def main(address: tuple) -> None:
    server = await asyncio.start_server(handler, *address)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    address = ("localhost", 5555)
    asyncio.run(main(address))
