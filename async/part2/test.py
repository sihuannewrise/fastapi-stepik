import asyncio


async def coro():
    print("вызов coro")
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError as error:
        print(error)
        print("перехватили отмену")
    print("завершение coro")


async def main():
    task = asyncio.create_task(coro())
    await asyncio.sleep(0)
    task.cancel("сообщение отмены!")
    await task


if __name__ == '__main__':
    asyncio.run(main())
