from inspect import getgeneratorstate

def echo_gen():
    while True:
        try:
            n = yield n
        except Exception as e:
            er_type = type(e)
            if er_type == StopIteration:
                return f"{er_type.__name__}. Генератор завершил свою работу!"
            else:
                n = yield f"Получено переданное исключение. Тип: {er_type.__name__}. Сообщение: {ValueError(e)}"


g = echo_gen()

g.send(None)
print(g.send(1))
print(g.throw(ValueError("oops!")))  # выводится информация о переданном исключении и
print(g.send(2))  # генератор продолжает работать
print(g.send("kwa-kwa"))
try:
    g.throw(StopIteration)
except StopIteration as error:
    print(error)
print(getgeneratorstate(g))  # проверяем что генератор завершил работу после передачи StopIteration
