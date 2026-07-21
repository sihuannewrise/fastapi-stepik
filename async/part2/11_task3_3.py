import asyncio
from typing import Callable
import time


async def sleep_with_callback(delay, func: Callable = None):
    await asyncio.sleep(delay)
    return func()

async def coroutine_1():
    result = await sleep_with_callback(2, lambda: "Результат 1")
    print(f"Корутина 1 вернула: {result}")

async def coroutine_2():
    result = await sleep_with_callback(1, lambda: "Результат 2")
    print(f"Корутина 2 вернула: {result}")

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(coroutine_1())
        tg.create_task(coroutine_2())

if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"All done in {time.perf_counter() - start_time:.2f}")
