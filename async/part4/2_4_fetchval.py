import asyncpg
import asyncio

RANGE = 10_000

async def main():
    conn: asyncpg.Connection = await asyncpg.connect(dsn="postgresql://postgres:postgres@169.254.1.2:5433/demo")
    result = await conn.fetchval("SELECT * FROM bookings.aircrafts_data WHERE range>$1",
                                 RANGE,
                                 column=1,
                                 )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
