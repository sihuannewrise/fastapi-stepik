import asyncio
from concurrent.futures import ThreadPoolExecutor

entities = []


async def main():
    blocking = []
    bt = []
    async_coros = []
    results = []
    loop = asyncio.get_running_loop()
    for entity in entities:
        if asyncio.iscoroutine(entity):
            async_coros.append(entity)
        else:
            blocking.append(entity)
    with ThreadPoolExecutor(len(blocking)) as executor:
        for blocking_task in blocking:
            bt.append(loop.run_in_executor(executor, blocking_task))
        all_tasks = bt + async_coros
        for task in asyncio.as_completed(all_tasks):
            res = await task
            results.append(res)
    print(results)


if __name__ == '__main__':
    asyncio.run(main())