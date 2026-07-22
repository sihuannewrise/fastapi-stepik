import contextvars
import asyncio
from itertools import count

_count = count(1)


async def task():
    n = next(_count)

    ctx = asyncio.current_task().get_context()
    print(list(ctx.items()))

    ctx_int.set(n)
    print(list(ctx.items()))
    print()
    await asyncio.sleep(n/10)
    print(f"task ctx_int,\tn = {ctx_int.get()}")


# {
async def main():
    ctx1 = contextvars.Context()
    ctx1.run(ctx_int.set, 3)
    # print(list(ctx.items()))

    ctx2 = contextvars.Context()
    ctx2.run(ctx_int.set, 2)

    ctx3 = contextvars.Context()
    ctx3.run(ctx_int.set, 1)

    task_1 = asyncio.create_task(task(), context=ctx1)
    task_2 = asyncio.create_task(task(), context=ctx2)
    task_3 = asyncio.create_task(task(), context=ctx3)
    await task_3
# }


if __name__ == '__main__':
    ctx_int = contextvars.ContextVar("num")
    ctx_int.set(0)
    ctx = contextvars.copy_context()
    with asyncio.Runner() as runner:
        runner.run(main(), context=None)
        print(f"runner ctx_int, n = {ctx_int.get()}")
