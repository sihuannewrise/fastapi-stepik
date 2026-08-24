import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Callable

entities = []


async def wrapper(f: Callable, tp: ThreadPoolExecutor, pp: ProcessPoolExecutor):
    loop = asyncio.get_running_loop()
    msg = "{} завершена с результатом {}"
    func_name = None
    result = None
    try:
        if asyncio.iscoroutine(f):
            func_name = "Корутина"
            result = await f
        elif getattr(f, "cpu", None):
            func_name = "Расчетная задача"
            result = await loop.run_in_executor(pp, f)
        else:
            func_name = "Блокирующая задача"
            result = await loop.run_in_executor(tp, f)
    except Exception as ex:
        result = f"{ex!r}"
    print(msg.format(func_name, result))


async def main():
    with ThreadPoolExecutor() as tp, ProcessPoolExecutor() as pp:
        for res in asyncio.as_completed([wrapper(f, tp, pp) for f in entities]):
            await res


if __name__ == "__main__":
    asyncio.run(main())
