import asyncpg
import asyncio
import time


async def some_work():
    print("Делаем что-то полезное пока ждем подключения...")
    somthing = await asyncio.sleep(0.1, "'Полезное'")
    print(f"Сделали что-то {somthing}")


async def connection():
    conn: asyncpg.connection.Connection = await asyncpg.connect(host="169.254.1.2",
                                                                port=5433,
                                                                user="postgres",
                                                                password="postgres",
                                                                database="demo")
    print(f"Подключение по адресу {conn._addr} установлено!")

    # Еще не проходили. Выполняем запрос, чтобы получить имя БД
    db_name = await conn.fetchval("SELECT current_database()")
    print(f"Подтверждаем, что подключились к БД: {db_name}")


async def main():
    await asyncio.gather(connection(), some_work())


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Выполнили за {time.perf_counter()-start_time:.2f}c")