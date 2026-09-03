import asyncio
import time

condition = asyncio.Condition()


async def coro_wait():
    async with condition:
        print(f"[1], {condition}")
        try:
            await asyncio.wait_for(condition.wait(), timeout=3)
        except TimeoutError:
            print("Вышли по таймеру!")
        print(f"[6], {condition}")
    print(f"[7], {condition}")


async def coro_notify():
    print(f"[2], {condition}")

    await condition.acquire()
    print(f"[3], {condition}")
    condition.notify_all()
    print(f"[4], {condition}")
    await asyncio.sleep(5)
    condition.release()

    print(f"[5], {condition}")


async def main():
    await asyncio.gather(coro_wait(), coro_notify())

if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Выполнилось за {time.perf_counter() - start_time:.1f}c.")
