import contextvars
import asyncio
from itertools import count

_count = count(1)


async def task():
    n = next(_count)
    ctx_int.set(n)
    await asyncio.sleep(n/10)
    print(f"task ctx_int,\tn = {ctx_int.get()}")


async def main():
    task_1 = asyncio.create_task(task(), context=None)
    task_2 = asyncio.create_task(task(), context=None)
    task_3 = asyncio.create_task(task(), context=ctx)
    await task_3


if __name__ == '__main__':
    ctx_int = contextvars.ContextVar("num")
    ctx_int.set(0)
    ctx = contextvars.copy_context()
    with asyncio.Runner() as runner:
        # {
        runner.run(main(), context=None)  # <- здесь?
        print(f"runner ctx_int, n = {ctx.get(ctx_int)}")  # <- или здесь?
        # }
