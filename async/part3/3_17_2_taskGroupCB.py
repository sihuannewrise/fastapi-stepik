import asyncio
import time


async def coro(i):
    return await asyncio.sleep(i/10, i)


def callback(task: asyncio.Task):
    print(f"Задача {task.get_name()} завершилась успешно с результатом {task.result()}")


class TaskGroupCB:

    def __init__(self, callback):
        self._callback = callback
        self._tasks = []

    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)


    def create_task(self, coro, *, name=None):
        task = asyncio.create_task(coro)
        if name:
            task.set_name(name)
        self._tasks.append(task)

        def done_callback(t):
            self._callback(t)
            try:
                self._tasks.remove(t)
            except ValueError:
                pass

        task.add_done_callback(done_callback)
        return task


async def main():
    async with TaskGroupCB(callback) as tgc:
        for n in range(10):
            tgc.create_task(coro(n), name=f"task#{n}")


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"\nAll done in {time.perf_counter() - start_time:.2f}с.")