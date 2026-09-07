import asyncio
from itertools import count

_count = count()


async def coro(barrier: asyncio.Barrier):
    task_name = asyncio.current_task().get_name()
    # каждая задача спит чуть дольше, для наглядного упорядоченного вывода
    await asyncio.sleep(next(_count)/10)
    print(f"-> Задача {task_name} достигла барьер")
    await barrier.wait()
    print(f"\t<- Задача {task_name} преодолела барьер")


async def main():
    barrier = asyncio.Barrier(3)
    tasks = [asyncio.create_task(coro(barrier)) for _ in range(4)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
