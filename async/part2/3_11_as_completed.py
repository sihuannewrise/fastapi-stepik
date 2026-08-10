import asyncio


async def main(aws, *, timeout=None):
    for aw in asyncio.as_completed(aws, timeout=timeout):
        try:
            print(await aw)
        except TimeoutError:
            print("Завершение по таймауту!")
            break
        except Exception as error:
            print(error)


if __name__ == '__main__':
    asyncio.run(main())
