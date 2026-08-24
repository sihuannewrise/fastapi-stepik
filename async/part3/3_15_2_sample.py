import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import inspect
from typing import TypedDict
from types import FunctionType, CoroutineType
from collections.abc import Sequence
import time
from functools import partial


class TasksByTypes(TypedDict):
    coros: list[CoroutineType]
    cpu_bound: list[FunctionType]
    io_bound: list[FunctionType]


def sort_objects_by_types(entities: Sequence[CoroutineType | FunctionType]) -> TasksByTypes:
    tasks_by_types: TasksByTypes = {
        'coros': [],
        'cpu_bound': [],
        'io_bound': []
    }
    for obj in entities:
        if inspect.iscoroutine(obj):
            tasks_by_types['coros'].append(obj)
        elif inspect.isfunction(obj):
            if hasattr(obj, 'cpu'):
                tasks_by_types['cpu_bound'].append(obj)
            else:
                tasks_by_types['io_bound'].append(obj)
    return tasks_by_types


def callback(aw: asyncio.Task | asyncio.Future, task_type: str):
    base_message = f"{task_type} завершена с результатом %s"
    try:
        print(base_message % aw.result())
    except (Exception, BaseException) as error:
        print(base_message % repr(error))


async def main():
    objects_by_types = sort_objects_by_types(entities=entities)
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=len(objects_by_types['io_bound'])) as tpe, ProcessPoolExecutor() as ppe:
        tasks = []
        for io_bound_object in objects_by_types['io_bound']:
            task = loop.run_in_executor(tpe, io_bound_object)
            task.add_done_callback(partial(callback, task_type="Блокирующая задача"))
            tasks.append(task)
        for cpu_bound_object in objects_by_types['cpu_bound']:
            task = loop.run_in_executor(ppe, cpu_bound_object)
            task.add_done_callback(partial(callback, task_type="Расчетная задача"))
            tasks.append(task)
        for coro in objects_by_types['coros']:
            task = loop.create_task(coro)
            task.add_done_callback(partial(callback, task_type="Корутина"))
            tasks.append(task)
        await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())
