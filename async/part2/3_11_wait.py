import asyncio


async def wait_tasks(tasks: list[asyncio.Task], timeout: float | int) -> tuple[dict, set]:
    res = {}
    done, pending = await asyncio.wait(tasks, timeout=timeout)
    for t in done:
        try:
            res[t.get_name()] = t.result()
        except asyncio.CancelledError:
            res[t.get_name()] = "Cancelled"
        except BaseException as error:
            res[t.get_name()] = error
    return res, pending


async def main():
    tasks = [asyncio.create_task(...) for ... in ...]
    results, not_done_tasks = await wait_tasks(tasks, timeout=...)

    for k, v in sorted(results.items()):
        print(f"{k}: {repr(v)}")


if __name__ == '__main__':
    asyncio.run(main())
