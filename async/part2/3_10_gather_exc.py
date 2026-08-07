import asyncio

coroutines = []
all_results = {}


def cb(task: asyncio.Task) -> None:
    coro_name = task.get_coro().__name__
    try:
        all_results[f"Task_{coro_name}"] = task.result()
    except BaseException as error:
        all_results[f"Task_{coro_name}"] = (f"repr(error)!\r")


async def main():
    tasks = [asyncio.create_task(coro) for coro in coroutines]
    for task in tasks:
        task.add_done_callback(cb)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
