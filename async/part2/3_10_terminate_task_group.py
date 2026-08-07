import asyncio

class AlarmOverheatException(Exception):
    """Exception raised to terminate a task group."""

async def service_diag():
    """Used to force termination of a task group."""
    raise AlarmOverheatException()


async def main(coroutines):
    try:
        async with asyncio.TaskGroup() as group:
            for coro in coroutines:
                group.create_task(coro)
            group.create_task(service_diag())
    except* AlarmOverheatException:
        print("WARNING: Критическая нагрузка, текущие задачи группы отменены!")
    except* Exception as exc:
        print(*exc.exceptions)

asyncio.run(main())