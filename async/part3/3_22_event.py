import asyncio

async def json_gen(): pass
async def registrator(): pass
def final(): pass


async def producer(queue: asyncio.LifoQueue, stop_event: asyncio.Event):
    async for elem in json_gen():
        await queue.put(elem)
    stop_event.set()


async def consumer(queue: asyncio.LifoQueue, stop_event: asyncio.Event):
    while True:
        if stop_event.is_set() and queue.empty():
            break
        elem = await queue.get()
        await registrator(elem)
        queue.task_done()


async def producer_consumer(queue: asyncio.LifoQueue):
    stop_event = asyncio.Event()
    [asyncio.create_task(consumer(queue, stop_event)) for _ in range(2)]
    await asyncio.create_task(producer(queue, stop_event))
    await queue.join()
    final()
