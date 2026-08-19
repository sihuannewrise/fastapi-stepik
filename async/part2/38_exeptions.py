import asyncio
import time


async def coro_1():
    await asyncio.sleep(1)
    print("корутина №1 выполнена")


async def coro_2():
    await asyncio.sleep(3)
    print("корутина №2 выполнена")


async def main():
    try:
        async with asyncio.timeout(2):
            task_1 = asyncio.create_task(coro_1())
            shield = asyncio.shield(coro_2())
            await task_1
            await shield
    except TimeoutError:
        print("Вышли по таймауту!")
    print(f"Задача №1 отменена? {task_1.cancelled()}")
    print(f"Задача №2 отменена? {shield.cancelled()}")

if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"\nAll done in {time.perf_counter() - start_time:.2f}")
