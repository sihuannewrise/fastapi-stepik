import asyncio
import concurrent.futures
import time


def cpu_bound():
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()

    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await asyncio.gather(*(loop.run_in_executor(pool, cpu_bound) for _ in range(8)))
        print(f"Пул потоков выполнил расчет, результат {result}")
    print(f"За {time.perf_counter() - start_time:.2f}с.")

    start_time = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await asyncio.gather(*(loop.run_in_executor(pool, cpu_bound) for _ in range(8)))
        print(f"Пул процессов выполнил расчет, результат {result}")
    print(f"За {time.perf_counter() - start_time:.2f}с.")

    start_time = time.perf_counter()
    with concurrent.futures.InterpreterPoolExecutor() as pool:
        result = await asyncio.gather(*(loop.run_in_executor(pool, cpu_bound) for _ in range(8)))
        print(f"Пул интерпретаторов выполнил расчет, результат {result}")
    print(f"За {time.perf_counter() - start_time:.2f}с.")

if __name__ == '__main__':
    asyncio.run(main())
