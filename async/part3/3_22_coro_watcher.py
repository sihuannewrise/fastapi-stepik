import asyncio

async def spider(): pass
async def scrap(): pass


new_items_arrived = asyncio.Event()
queue = asyncio.Queue()


async def coro_watcher():
    while not new_items_arrived.is_set():
        await asyncio.sleep(0.1)
        response = await scrap()
        if not response:
            continue
        for item in response["new"]:
            await queue.put(item)
        new_items_arrived.set()


async def coro_handler():
    await new_items_arrived.wait()
    item = queue.get_nowait()
    await spider(item)
    queue.task_done()


async def main_logic():
    await asyncio.create_task(coro_watcher())
    await asyncio.gather(*[asyncio.create_task(coro_handler()) for _ in range(5)])
