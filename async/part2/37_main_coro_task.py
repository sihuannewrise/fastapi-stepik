import asyncio
import time

async def coro_1():
    await asyncio.sleep(1)


async def coro_2():
    print("Все активные задачи:")
    for i, t in enumerate(asyncio.all_tasks(), 1):
        print(f"Задача № {i}\t", t)
    await asyncio.sleep(2)


async def main():
    print(f"Имя задачи корутины main {asyncio.current_task().get_name()}")
    task_1 = asyncio.create_task(coro_1())
    task_2 = asyncio.create_task(coro_2())
    await task_2


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"\nAll done in {time.perf_counter() - start_time:.2f}")
    