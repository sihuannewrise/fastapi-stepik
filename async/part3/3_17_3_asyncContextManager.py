import asyncio
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

entities = []
n: int = 4


@asynccontextmanager
async def thread_executor(n_threads: int):
    executor = ThreadPoolExecutor(n_threads)
    try:
        yield executor
    finally:
        executor.shutdown(wait=False)




def cb(task: asyncio.Task | asyncio.Future):
    if not task.cancelled():
        try:
            print(task.result())
        except Exception as exc:
            print(f"Ошибка: {exc!r}")


async def main():
    loop = asyncio.get_running_loop()
    try:
        async with asyncio.TaskGroup() as tg, thread_executor(n) as thread_pool:
            for task in entities:
                if asyncio.iscoroutine(task):
                    tg.create_task(task).add_done_callback(cb)
                else:
                    loop.run_in_executor(thread_pool, task).add_done_callback(cb)
    except ExceptionGroup:
        pass


if __name__ == '__main__':
    asyncio.run(main())