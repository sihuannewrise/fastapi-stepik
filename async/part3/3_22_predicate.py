import asyncio

condition = asyncio.Condition()
n = 0


def predicate():
    global n
    n += 1
    print(f"Задача {asyncio.current_task().get_name()} вызвала предикат {n} раз")
    return n >= 7


async def coro_wait_for():
    async with condition:
        await condition.wait_for(predicate)


async def coro_notify():
    for i in range(1, 4):
        await asyncio.sleep(1)  # уведомляем каждую секунду!
        async with condition:
            print(f"Вызываем notify {i} раз")
            condition.notify(i)  # уведомляем разное количество ожидающих задачи!


async def main():
    # три ожидающих задачи!
    await asyncio.gather(coro_wait_for(), coro_wait_for(), coro_wait_for(), coro_notify())


if __name__ == '__main__':
    asyncio.run(main())
