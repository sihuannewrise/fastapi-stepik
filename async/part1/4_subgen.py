def coroutine(gen):
    def inner(*arg, **kwargs):
        g = gen(*arg, **kwargs)
        g.send(None)
        return g
    return inner



def sub_gen():
    while True:
        try:
            msg = yield  # получаем сообщение
        except Exception as err:
            print(f"Ошибка {err}")  # обрабатываем ошибку
        else:
            print(f"Сообщение {msg} получено!")  # имитируем обработку сообщения. полезная работа


@coroutine
def delegate_gen(g):
    yield from g


sg = sub_gen()
dg = delegate_gen(sg)

dg.send("msg_1")
dg.send("msg_2")
dg.throw(ValueError("my_error_msg!"))
