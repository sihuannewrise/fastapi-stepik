import asyncio


async def simple_gather(*coros_or_futures) -> list:
    tasks = [asyncio.ensure_future(coro) for coro in coros_or_futures]
    results = []
    for task in tasks:
        try:
            result = await task
            results.append(result)
        except Exception as exc:
            results.append(exc)
    return results
