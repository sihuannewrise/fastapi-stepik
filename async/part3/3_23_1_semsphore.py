import asyncio
from typing import Callable


class AsyncHubHandler():

    def __init__(self, limit: int, coro_function: Callable, n_tasks: int):
        self.limit = limit
        self.coro_function = coro_function
        self.n_tasks = n_tasks
        self.semaphore = asyncio.Semaphore(self.limit)

    async def run_task(self, coro):
        async with self.semaphore:
            await coro

    async def start_hub(self):
        coros = (self.coro_function() for _ in range(self.n_tasks))
        tasks = [asyncio.create_task(self.run_task(coro)) for coro in coros]
        await asyncio.gather(*tasks)
