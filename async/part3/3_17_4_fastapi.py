from fastapi import FastAPI, Depends, Request
import threading
import time
from itertools import count
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version
import asyncio
from functools import partial

N = 45  # количество одновременных запросов
count_ = count(1)  # для вывода количества обработанных запросов

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"FastAPI version: {version('fastapi')}", flush=True)
    print(f"Uvicorn version: {version('uvicorn')}", flush=True)
    app.state.io_pool = ThreadPoolExecutor(max_workers=N, thread_name_prefix="io_thread")
    yield
    app.state.io_pool.shutdown(wait=True, cancel_futures=True)

app = FastAPI(lifespan=lifespan)

async def get_executor(request: Request):
    pool = request.app.state.io_pool

    async def executor(func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(pool, partial(func, *args, **kwargs))

    return executor

def blocking_task():
    time.sleep(0.5)
    return {"thread_name": threading.current_thread().name, "threads": threading.active_count()}

@app.get("/")
async def read_root(executor=Depends(get_executor)):
    data = await executor(blocking_task)
    return {"n": next(count_), "data": data}
