import asyncio
import sys


async def sub_proc(code: str) -> str:
    process = await asyncio.create_subprocess_exec(sys.executable, '-c',
                                                   code,
                                                   stdout=asyncio.subprocess.PIPE)
    data_output, _ = await process.communicate()
    line = data_output.decode().rstrip()

    return line