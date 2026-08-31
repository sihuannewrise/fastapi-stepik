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
    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [asyncio.create_task(consumer(queue)) for _ in range(2)]

    await producer_task
    await queue.join()

    for task in consumer_tasks:
        task.cancel()

    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    final()
