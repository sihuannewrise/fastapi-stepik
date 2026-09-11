import asyncpg
import asyncio
import time

N_SIZE = 10  # размер пула (количество созданных подключений)


async def main():
    async with asyncpg.create_pool(
            host="169.254.1.2",
            port=5433,
            user="postgres",
            password="postgres",
            database="demo",
            min_size=N_SIZE,
            max_size=N_SIZE) as pool:
        print(f"Всего свободных соединений в пуле перед запросом: {pool.get_idle_size() = }")
        async with pool.acquire() as conn:
            db_name = await conn.fetchval("SELECT current_database()")
            print(f"Подтверждаем, что подключились к БД: {db_name}")
            print("Всего свободных соединений в пуле:", pool.get_idle_size())
        print(f"Всего свободных соединений в пуле после release: {pool.get_idle_size() = }")


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Выполнили за {time.perf_counter() - start_time:.2f}c")
