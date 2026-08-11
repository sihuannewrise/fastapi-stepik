import asyncio

results = []

def cb(task: asyncio.Task) -> None:
    if not task.cancelled():
        results.append(task.get_coro().__name__)


async def main(coroutines: list) -> list[str]:
    for coro in coroutines:
        if coro.__name__ == "response_limit":
            delay_task = asyncio.create_task(coro)
            coroutines.remove(coro)
    delay = await delay_task

    try:
        async with asyncio.timeout(delay):
            tasks = [asyncio.create_task(coro) for coro in coroutines]
            for task in tasks:
                task.add_done_callback(cb)
                await task
    except TimeoutError:
        pass
    return results
