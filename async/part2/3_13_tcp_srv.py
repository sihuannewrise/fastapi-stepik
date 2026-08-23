import asyncio

def worker(): pass

async def shutdown_server(server: asyncio.Server) -> None:
    await asyncio.sleep(1)
    while True:
        if not hasattr(server, '_connections') or len(server._connections) == 0:
            server.close()
            await server.wait_closed()
            raise asyncio.CancelledError()
        await asyncio.sleep(1)


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = await reader.read(1024)
    res = await worker(data.decode())
    writer.write(res.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main(address: tuple) -> None:
    server = await asyncio.start_server(handler, *address)
    async with server:
        asyncio.create_task(shutdown_server(server))
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            print("Работа сервера завершена!")
