import asyncio
import types, time


@types.coroutine # декоратор переопределяет методы генератора в методы корутины
def gen_num():
    for i in range(1, 5):
        print(i, end=" ")
        yield


@types.coroutine
def gen_str():
    for s in "abcd":
        print(s, end=" ")
        yield


async def coro_1():
    print("my_coroutine_1 start")
    await asyncio.sleep(1)
    await gen_num()
    print("my_coroutine_1 end")


async def coro_2():
    print("my_coroutine_2 start")
    await asyncio.sleep(1)
    await gen_str()
    print("my_coroutine_2 end")


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(coro_1())
        tg.create_task(coro_2())
        print(len(asyncio.all_tasks()))


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"All done in {time.perf_counter() - start_time:.2f}")
