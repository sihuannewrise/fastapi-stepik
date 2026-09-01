import asyncio
from time import perf_counter


sources = ["https://www.yahoo.com",
           "https://www.yahoo.com",
           "https://www.bing.com",
           "https://www.yahoo.com",
           "https://www.bing.com",
           "https://www.yahoo.com",
           "https://www.bing.com"]


cache_data = dict()  # <-! Кэш

lock = asyncio.Lock()  # <-! Примитив синхронизации


async def get_headers(url: str) -> dict:
    async with lock:
        if url not in cache_data:
            print(f"Данных по {url} нет в кэше")
            cache_data[url] = await get_headers_request(url)
        else:
            print(f"Данные по {url} взяли из кэша")
        return cache_data[url]


async def get_headers_request(url: str) -> dict:
    print(f"Выполняется запрос по адресу {url}")
    headers = {}
    _, hostname = url.rsplit("//")
    reader, writer = await asyncio.open_connection(hostname, 443, ssl=True)
    query = f"HEAD / HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
    writer.write(query.encode())
    await writer.drain()
    while True:
        line = await reader.readline()
        text = line.decode().rstrip()
        if not text:
            break
        try:
            k, v = text.split(": ", 1)
            headers[k] = v
        except ValueError:
            pass
    writer.close()
    return headers


async def main():
    tasks = [get_headers(source) for source in sources]  # <-! Задачи на основе новой корутины
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


if __name__ == '__main__':
    start_time = perf_counter()
    results = asyncio.run(main())
    print(f"Выполнено за: {perf_counter() - start_time:.2f}с.")
