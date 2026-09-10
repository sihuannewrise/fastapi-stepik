from asyncpg import connect, Connection
from contextlib import asynccontextmanager


@asynccontextmanager
async def manage_connection(**kwargs):
    conn = await connect(**kwargs)
    try:
        yield conn
    finally:
        await conn.close()
