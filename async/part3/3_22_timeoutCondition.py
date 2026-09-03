import asyncio


class TimeoutCondition(asyncio.Condition):
    async def wait_for(self, predicate, timeout=None):
        if timeout is None:
            return await super().wait_for(predicate)
        try:
            return await asyncio.wait_for(super().wait_for(predicate), timeout=timeout)
        except asyncio.TimeoutError:
            return predicate()


condition = asyncio.TimeoutCondition()
