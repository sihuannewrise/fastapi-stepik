import asyncio
import time


async def coro():
    print("1")
    await asyncio.sleep(0)
    print("2")
    await asyncio.sleep(1)
    print("3")
    await asyncio.sleep(2)
    print("4")


class AsyncDelay:
    def __init__(self, delay):
        self.delay = delay

    async def __aenter__(self):
        await asyncio.sleep(self.delay)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"{exc_type.__name__}: {exc_value}")
        return True


async def main():
    task = asyncio.create_task(coro())
    async with AsyncDelay(1.5):
        raise ValueError("message error!")


if __name__ == '__main__':
    _start_time = time.perf_counter()
    asyncio.run(main())
    print(f"All done in {time.perf_counter() - _start_time:.1f}c.")
