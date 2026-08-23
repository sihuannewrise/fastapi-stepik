import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

entities = []


async def main():
    tasks = []
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as th_pool, ProcessPoolExecutor() as pr_pool:
        for entity in entities:
            if asyncio.iscoroutine(entity):
                tasks.append(asyncio.create_task(entity))
            elif hasattr(entity, "cpu"):
                tasks.append(loop.run_in_executor(pr_pool, entity))
            else:
                tasks.append(loop.run_in_executor(th_pool, entity))
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
