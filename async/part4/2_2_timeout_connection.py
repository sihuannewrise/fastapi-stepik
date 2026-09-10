from asyncpg import connect, Connection
from typing import Optional
import os


my_password = os.getenv('DB_PASSWORD', 'admin')


async def timeout_connection(timeout: float) -> Optional[Connection]:
    try:
        conn: Connection = await connect(
            port=5434,
            user="postgres",
            password=my_password,
            database="demo",
            timeout=timeout,
        )
        return conn
    except TimeoutError:
        print("Timeout! Не удалось установить соединение за заданное время!")
