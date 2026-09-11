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
            max_size=N_SIZE,
            max_queries=1) as pool:
        pool.set_connect_args(host="169.254.1.2", port="5433", user="knhdb1", password="knhdb1", database="knhdb1")

        db_name = await pool.fetchval("SELECT current_database()")
        print(f"Подтверждаем, что подключились к БД: {db_name}")

        db_name = await pool.fetchval("SELECT current_database()")
        print(f"Подтверждаем, что подключились к БД: {db_name}")



if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Выполнили за {time.perf_counter() - start_time:.2f}c")
