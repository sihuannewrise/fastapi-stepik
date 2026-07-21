import requests  # модуль требует установки!
from time import perf_counter
import threading


sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]

headers_stor = {}
start = perf_counter()
sum_ex_time = 0

def get_request_header(url: str) -> None:
   headers_stor[url] = requests.get(url).headers

threads = []

for source in sources:
    start_tmp = perf_counter()
    thread = threading.Thread(target=get_request_header, args=(source,))
    thread.start()
    delta = perf_counter() - start_tmp
    print(source, delta)
    sum_ex_time += delta
    threads.append(thread)

for thread in threads:
    thread.join()
    print(thread)

print(f"completed in {perf_counter()-start} seconds")  # Считаем общее время выполнения всех запросов
print(sum_ex_time)  # Показываем то, что общее время работы является простой суммой каждого запроса по отдельности
# print(*headers_stor.items(), sep="\n")  # Выводим наши заголовки
