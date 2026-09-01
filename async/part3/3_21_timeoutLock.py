import asyncio


class TimeoutLock(asyncio.Lock):
    async def acquire(self, timeout=None):
        if timeout is None:
            return await super().acquire()

        try:
            return await asyncio.wait_for(super().acquire(), timeout=timeout)
        except asyncio.TimeoutError:
            return False

lock = TimeoutLock()


async def coro(timeout=None):
    acquired = await lock.acquire(timeout)
    try:
        await cashed_request()
    finally:
        if acquired:
            lock.release()
