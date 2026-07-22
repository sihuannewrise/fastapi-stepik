import asyncio
import contextvars

int_ctx = contextvars.ContextVar("int_ctx", default=0)
int_global = 0


async def sub_coroutine():
    await asyncio.sleep(1)
    print(f'Число в контексте суб корутины: {int_ctx.get()}')
    print(f'Глобальное число в суб корутине: {int_global}')


async def main_coroutine(req_id):
    global int_global
    int_ctx.set(req_id)
    int_global = req_id
    await sub_coroutine()
    print(f'Число в контексте главной корутины: {int_ctx.get()}')
    print()


async def main():
    tasks = []
    for req_id in range(1, 4):
        tasks.append(asyncio.create_task(main_coroutine(req_id)))
    for task in tasks:
        await task


if __name__ == '__main__':
    asyncio.run(main())
