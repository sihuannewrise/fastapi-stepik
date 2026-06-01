def my_awesome_gen():
    res = 0
    while True:
        value = yield res
        if not isinstance(value,(int, float)):
            return "Ошибка: введите число типа int или float"
        if isinstance(value,int):
            res += value
        else:
            res *= value


g = my_awesome_gen()

print(g.send(None))  # Выводит 0
print(g.send(10))  # Выводит 10
print(g.send(11))  # Выводит 21
print(g.send(0.5))  # Выводит 10.5
print(g.send(100))  # Выводит 110.5
print(g.send("ok"))  # Возбуждается ошибка StopIteration: Ошибка: введите число типа int или float
