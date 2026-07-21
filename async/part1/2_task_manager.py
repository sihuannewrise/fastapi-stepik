from typing import Generator
import inspect
from collections import deque

def task_1():
    for i in range(1, 5):
        yield i


def task_2():
    for s in "AB":
        yield s

def g_task():
    yield 1
    n = yield 2
    print(n)
    yield 3
    return "Расчет окончен!"


g1 = task_1()
g2 = task_2()


def task_manager(tasks: tuple[Generator] | list[Generator]) -> None:
    deg = deque(tasks)
    while deg:
        task=deg.popleft()
        try:
            print(next(task))
        except StopIteration:
            print(f'Задача {task.__name__} завершена!')
        else:
            deg.append(task)

# print(dir(g1))
# task_manager((g1, g2))
g = g_task()
print(inspect.getgeneratorstate(g))

try:
    print(next(g))
    print(inspect.getgeneratorstate(g))
    print(next(g))
    g.send(3)
    next(g)
except StopIteration as error:
    print(error)

print(inspect.getgeneratorstate(g))
