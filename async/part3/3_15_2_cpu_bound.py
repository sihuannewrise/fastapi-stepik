import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial

entities = []

def cb(prefix, task):
    try:
        print(f"{prefix} завершена с результатом {task.result()}")
    except Exception as e:
        print(f"{prefix} завершена с результатом {repr(e)}")


async def main():
    tasks = []
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as th_pool, ProcessPoolExecutor() as pr_pool:
        for entity in entities:
            if asyncio.iscoroutine(entity):
                task = asyncio.create_task(entity)
                task.add_done_callback(partial(cb, "Корутина"))
                tasks.append(task)
            elif hasattr(entity, "cpu"):
                future = loop.run_in_executor(pr_pool, entity)
                future.add_done_callback(partial(cb, "Расчетная задача"))
                tasks.append(future)
            else:
                future = loop.run_in_executor(th_pool, entity)
                future.add_done_callback(partial(cb, "Блокирующая задача"))
                tasks.append(future)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            pass


if __name__ == '__main__':
    asyncio.run(main())
