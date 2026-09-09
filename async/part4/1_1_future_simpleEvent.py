import asyncio
import collections


class SimpleEvent:
    def __init__(self):
        self._waiters = collections.deque()

    async def wait(self):
        fut = asyncio.get_running_loop().create_future()
        self._waiters.append(fut)
        try:
            await fut
        finally:
            if fut in self._waiters:
                self._waiters.remove(fut)

    def set(self):
        while self._waiters:
            future = self._waiters.popleft()
            if not future.done():
                future.set_result(None)
