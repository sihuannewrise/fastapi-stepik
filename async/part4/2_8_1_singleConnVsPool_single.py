import asyncpg
import asyncio
import time
from datetime import datetime


async def execute_query(start, end):
    conn = await asyncpg.connect(
        host="169.254.1.2",
        port=5433,
        user="postgres",
        password="postgres",
        database="demo",)
    try:
        return await conn.fetchval("""SELECT COUNT(*), pg_sleep(0.1) FROM bookings.bookings
                                      WHERE book_date BETWEEN $1 AND $2""", start, end)
    finally:
        await conn.close()


async def main():
    dates = [(datetime(2017, 6, 25), datetime(2017, 6, 26)),
             (datetime(2017, 7, 25), datetime(2017, 7, 26)),
             (datetime(2017, 8, 15), datetime(2017, 8, 16))] * 16  # всего 90 запросов

    results = await asyncio.gather(*(execute_query(start, end) for start, end in dates))
    return results


if __name__ == '__main__':
    start_time = time.perf_counter()
    results = asyncio.run(main())
    print(f"Без пула: Выполнено {len(results)} запросов за {time.perf_counter() - start_time:.2f}c")