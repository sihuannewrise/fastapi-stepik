import contextvars
import asyncio


async def task():
    await asyncio.sleep(0.1)
    print(f"task ctx_int,\tn = {ctx_int.get()}")
    print(f"task ctx,\t\tn = {ctx[ctx_int]}")


async def main():
    ctx_int.set(1)
    await asyncio.create_task(task())


if __name__ == '__main__':
    ctx_int = contextvars.ContextVar("num")
    ctx_int.set(0)
    ctx = contextvars.copy_context()
    with asyncio.Runner() as runner:
        runner.run(main(), context=None)
        print(f"runner ctx_int, n = {ctx[ctx_int]}")
        print()
        runner.run(main(), context=ctx)
        print(f"runner ctx_int, n = {ctx[ctx_int]}")
