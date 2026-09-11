import asyncpg
import asyncio


async def main():
    async with asyncpg.create_pool(
                host="169.254.1.2",
                port=5433,
                user="postgres",
                password="postgres",
                database="demo",
                max_inactive_connection_lifetime=2) as pool:
        await asyncio.sleep(1)
        connections = [await pool.acquire() for _ in range(3)]
        for conn in connections:
            print("PID backend-процесса:", await conn.fetchval('SELECT pg_backend_pid()'))
            await pool.release(conn)

        print(f"{pool.get_idle_size() = }")

        await asyncio.sleep(1.5)
        connections = [await pool.acquire() for _ in range(3)]
        for conn in connections:
            print("PID backend-процесса:", await conn.fetchval('SELECT pg_backend_pid()'))
        print(f"{pool.get_idle_size() = }")
        for conn in connections:
            await pool.release(conn)


if __name__ == '__main__':
    asyncio.run(main())
