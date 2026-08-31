import asyncio

async def json_gen(): pass
async def final(): pass
async def registrator(): pass


async def producer(queue: asyncio.Queue):
    async for elem in json_gen():
        await queue.put(elem)


async def consumer(queue: asyncio.Queue):
    while True:
        elem = await queue.get()
        await registrator(elem)
        queue.task_done()


async def producer_consumer(queue: asyncio.Queue):
    await asyncio.gather(consumer(queue), consumer(queue))
    await asyncio.create_task(producer(queue))
    await queue.join()
    final()
