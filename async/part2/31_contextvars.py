import contextvars
import asyncio


ctx_var = contextvars.ContextVar("sample")
ctx_var.set("global")
ctx_global = contextvars.copy_context()


async def task():
    ctx = asyncio.current_task().get_context()
    ctx_var.set("task")  # <-!
    print(f"Задача task: {ctx is ctx_global = }, {ctx[ctx_var] = }")


async def main():
    ctx = asyncio.current_task().get_context()
    ctx_var.set("main")  # <-!
    await asyncio.create_task(task())
    print(f"Задача main: {ctx is ctx_global = }, {ctx[ctx_var] = }")


if __name__ == '__main__':
    with asyncio.Runner() as runner:
        runner.run(main())
