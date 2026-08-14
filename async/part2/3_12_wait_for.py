import asyncio

async def response_limit(): pass


async def main(coroutine):
    task1 = asyncio.create_task(coroutine)
    task2 = asyncio.create_task(response_limit())
    delay = await task2
    try:
        result =  await asyncio.wait_for(task1, delay)
    except TimeoutError:
        return None, print("\nЗадача отменена, превышено время ожидания!")
    return result
