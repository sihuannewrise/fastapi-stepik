from itertools import count


def g_average():
    counter = count(1)
    res = None
    res = yield res
    while True:
        try:
            avg = res/next(counter)
            res += yield avg
        except Exception as e:
            return avg, type(e).__name__, ValueError(e)

g = g_average()

print(g.send(None))  # выводит None
print(g.send(0))  # выводит 0.0
print(g.send(10))  # выводит 5.0, т.к. (0 + 10) / 2
print(g.send(20))  # выводит 10.0, т.к. (0 + 10 + 20) / 3
print(g.send(0))  # выводит 7.5
try:
    g.throw(ValueError("new_throw_msg"))
except StopIteration as err:  # здесь обрабатываем завершение генератора
    avr, err, msg = err.value
    print(avr, err, msg)  # выводит три значения через пробел: 7.5 ValueError new_throw_msg
