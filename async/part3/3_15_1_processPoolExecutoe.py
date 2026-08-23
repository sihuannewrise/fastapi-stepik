import asyncio
from concurrent.futures import ProcessPoolExecutor

entities = []


async def main():
    all_tasks = []
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        for entity in entities:
            if asyncio.iscoroutine(entity):
                all_tasks.append(asyncio.create_task(entity))
            else:
                all_tasks.append(loop.run_in_executor(pool, entity))
        await asyncio.gather(*all_tasks)


if __name__ == '__main__':
    asyncio.run(main())
