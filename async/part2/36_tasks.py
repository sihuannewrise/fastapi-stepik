import asyncio
import time
import types


async def short_coro():
    for i in range(5):
        await asyncio.sleep(0)
        print(f"short\t{i=}")
    return "short"


async def long_coro():
    for i in range(10, 20):
        await asyncio.sleep(0)
        print(f"long\t{i=}")
    return "long"


def callback_task_1(task: asyncio.Task):
    print(f"Вызван коллбэк №1 с именем задачи {task.get_name()}")


def callback_task_2(task: asyncio.Task):
    print(f"Задача завершена? {task.done()=}")
    print(f"Задача отменена? {task.cancelled()=}")


async def main():
    task_1 = asyncio.create_task(short_coro())
    task_2 = asyncio.create_task(long_coro())
    task_2.add_done_callback(callback_task_1)
    task_2.add_done_callback(callback_task_2)
    await task_1
    # task_2.cancel()


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"all done in {time.perf_counter() - start_time:.2f}")
