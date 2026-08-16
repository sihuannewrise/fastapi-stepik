import asyncio
import json
from time import perf_counter

sources = [
    "https://query1.finance.yahoo.com/v8/finance/chart/RACE",
    "https://query1.finance.yahoo.com/v8/finance/chart/TSLA"]

user_agent_key = "User-Agent"
user_agent_value = "Mozilla/5.0"


async def get_json(url: str) -> tuple[str, dict]:
    # Получаем путь из URL
    path = url.split("//", 1)[1]  # Это даст нам 'query1.finance.yahoo.com/v8/finance/chart/RACE'

    # Отделяем путь от хоста
    host = "query1.finance.yahoo.com"
    request_path = f"/{path.split('/', 1)[1]}"  # Даем путь без домена

    reader, writer = await asyncio.open_connection(host, 443, ssl=True)

    # Формируем GET запрос с включением User-Agent
    request = f"GET {request_path} HTTP/1.1\r\n" \
              f"Host: {host}\r\n" \
              f"Accept: application/json\r\n" \
              f"{user_agent_key}: {user_agent_value}\r\n" \
              f"Connection: close\r\n" \
              f"\r\n"

    writer.write(request.encode())
    await writer.drain()
    # Читаем заголовки
    headers = b""
    while True:
        line = await reader.readline()
        headers += line
        if line == b"\r\n":  # Конец заголовков
            break
    # Проверяем статус
    if b"HTTP/1.1 200 OK" not in headers:
        print(f"Ошибка при получении ответа от {url}")
        return url, {}
    # Читаем тело ответа запроса
    body = b""
    while True:
        chunk = await reader.read(4096)
        if not chunk:
            break
        body += chunk
    # Выделяем данные из тела ответа
    parts = body.split(b"\r\n")
    json_body = parts[1] if len(parts) > 1 else body  # костыль, если в теле ответа нет информации о size
    json_data = json.loads(json_body)
    print(f"Ответ от {url} получен")
    return url, json_data


async def main():
    tasks = [get_json(source) for source in sources]
    results = await asyncio.gather(*tasks)
    json_stor = {}
    for url, json_data in results:
        json_stor[url] = json_data
        # Печатаем данные json ответа, например, имя компании, валюту торгов и последнюю цену
        print(json_data["chart"]["result"][0]["meta"]["longName"], end=" ")
        print(json_data["chart"]["result"][0]["meta"]["currency"], end=" ")
        print(json_data["chart"]["result"][0]["meta"]["previousClose"])


if __name__ == '__main__':
    start_time = perf_counter()
    asyncio.run(main())
    print(f"Выполнено за: {perf_counter() - start_time:.2f}с.")
