import asyncio

coroutines = []
results = []
cancelled = []

def handler(task: asyncio.Task):
    if not task.cancelled():
        if error := task.exception():
            results.append(error)
        else:
            results.append(task.result())
    else:
        cancelled.append(task.get_coro().__name__)

async def main():
    try:
        final_task = asyncio.create_task(coroutines[-1])
        final_task.add_done_callback(handler)
        async with asyncio.TaskGroup() as tg:
            for coro in coroutines[:-1]:
                tg.create_task(coro).add_done_callback(handler)
    except Exception:
        pass
    finally:
        await final_task


if __name__ == "__main__":
    asyncio.run(main())
