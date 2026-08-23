import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

entities = []

async def cb(task):



async def main():
    tasks = []
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as th_pool, ProcessPoolExecutor() as pr_pool:
        for entity in entities:
            if asyncio.iscoroutine(entity):
                tasks.append(asyncio.create_task(entity).add_done_callback(cb))
            elif hasattr(entity, "cpu"):
                tasks.append(loop.run_in_executor(pr_pool, entity).add_done_callback(cb))
            else:
                tasks.append(loop.run_in_executor(th_pool, entity).add_done_callback(cb))
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
