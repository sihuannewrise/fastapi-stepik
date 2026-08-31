import asyncio


AsyncQueueType = asyncio.Queue | asyncio.LifoQueue | asyncio.PriorityQueue


async def json_gen(): pass

async def consumer(queue):
    task_name = asyncio.current_task().get_name()

    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=0.2)
            print(f"{task_name} извлек элемент очереди {repr(item)}")
            queue.task_done()

        except TimeoutError:
            print(f"Работа {task_name} завершена!")
            return


async def producer(queue: AsyncQueueType):
    task = asyncio.current_task().get_name()
    async for i in json_gen():
        try:
            await asyncio.wait_for(queue.put(repr(i)), timeout=0.4)
            print(f"{task} поместил {repr(i)} в очередь")
        except TimeoutError:
            print(f"Очередь переполнена, требуется больше потребителей!")
            await queue.put(i)
            print(f"{task} поместил {repr(i)} в очередь")

