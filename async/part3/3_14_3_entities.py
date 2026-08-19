import asyncio

entities = []

async def main():
    tasks = []
    for obj in entities:
        if asyncio.iscoroutine(obj):
            tasks.append(asyncio.create_task(obj))
        else:
            tasks.append(asyncio.create_task(asyncio.to_thread(obj)))
    for task in tasks:
        await task

if __name__ == '__main__':
    asyncio.run(main())
