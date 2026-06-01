from typing import Callable, Generator


def sub_gen():
    total_sum = 0
    for i in range(1, 5):
        total_sum += i
        yield f"+{i}, sum={total_sum}"
    return total_sum


def handler(data):
    print(f"callback for {data}")  # имитируем обработку результата


# Ваше определение делегирующего генератора
def callback_delegate(g: Generator, func: Callable):
    res = yield from g
    return handler(res)


for elem in callback_delegate(sub_gen(), handler):
    print(elem)
