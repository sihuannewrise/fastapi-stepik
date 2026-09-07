import asyncio
import signal


async def coro():
    print("другая задача в работе")
    await asyncio.sleep(1)
    print("другая задача еще в работе")
    await asyncio.sleep(1)
    print("другая задача завершается")


async def sub_proc():
    code = "import datetime; import time; time.sleep(1); print(datetime.datetime.now())"
    process = await asyncio.create_subprocess_exec('python', '-c',
                                                   code, stdout=asyncio.subprocess.PIPE)
    print(process)
    process.send_signal(signal.SIGKILL)
    await asyncio.sleep(1)
    print(process.returncode)


async def main():
    await asyncio.gather(sub_proc(), coro())


if __name__ == '__main__':
    asyncio.run(main())
