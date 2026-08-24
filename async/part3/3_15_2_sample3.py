import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

entities = []


def cb(task: asyncio.Task | asyncio.Future):
    if exc := task.exception():
        result = repr(exc)
    else:
        result = task.result()
    print(f"{task.type_name} завершена с результатом {result}")


async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as th_pool, ProcessPoolExecutor() as pr_pool:
        io_futures = []
        cpu_futures = []
        async_coro = []
        for elem in entities:
            if asyncio.iscoroutine(elem):
                f = asyncio.create_task(elem)
                f.type_name = "Корутина"
                async_coro.append(f)
                f.add_done_callback(cb)
            elif hasattr(elem, "cpu"):
                f = loop.run_in_executor(pr_pool, elem)
                f.type_name = "Расчетная задача"
                cpu_futures.append(f)
                f.add_done_callback(cb)
            else:
                f = loop.run_in_executor(th_pool, elem)
                f.type_name = "Блокирующая задача"
                io_futures.append(f)
                f.add_done_callback(cb)
        await asyncio.gather(*io_futures, *cpu_futures, *async_coro, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
